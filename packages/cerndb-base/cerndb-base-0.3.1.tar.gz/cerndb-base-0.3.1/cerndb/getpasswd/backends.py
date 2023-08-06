"""get_passwd backends

Raises:
    BackendException: a generic exception
    PasswordDirectoryException: when password_directory doesn't exist
    IOError: when password file exists but cannot be opened from a reason
        different than access denied
    InvalidConfigurationException: missing key in the config file
"""
from abc import ABCMeta, abstractmethod
import os
import errno
import getpass
import argparse
import re
from pathlib import Path
from requests import get
from cerndb.config import CFG, Config
from cerndb.log import logger, setup_root_logger


class InvalidConfigurationException(Exception):
    """Raised when Config file is missing fields."""


class BackendException(Exception):
    """
    Any exception that we expect to happen, and it stops
        further processing. To be caught in main (console runner)
    """


class PasswordDirectoryException(BackendException):
    """
    Raised when specified password_directory doesn't exist
    """


class StatusCodeException(BackendException):
    """
    Raised when GET request returns something else than 200 or 404
    """


class Backend(metaclass=ABCMeta):
    """
    Abstract Backend class, all get_passwd backends should
    inherit from it
    """

    def __init__(self, config=None, settings=None):
        """Read configuration.

        Args:
            config (cerndb.config.Config, optional): Config object to use.
                Defaults to None.
            settings: dict
                Allows to override config file arguments from child class
                    before performing validation
        """
        # User provided or default config
        if config is None:
            self.config = CFG
        else:
            self.config = config
        # Replace config values with what comes from children
        if isinstance(self.config, Config):
            self.config.set_args(settings)
        # validate_config which can be implemented by child classes
        self.validate_config()
        setup_root_logger(self.config,
                          tag="getpasswd.backends.{self.__class__.__name__}")

    def validate_config(self):
        """
        Base implementation of validation. Just check
        if dictionary was given
        """
        if not isinstance(self.config, Config):
            raise InvalidConfigurationException(
                "Incorrect configuration, expected cerndb.config.Config object"
                ", got: {}".format(self.config))

    @classmethod
    def parse_arguments(cls, args):
        """Parse command-line arguments. Child class must implement."""
        if args is not None:
            raise BackendException("Not implemented!")
        return {}

    @abstractmethod
    def get(self, password_tag):
        """Get a password from a password tag."""
        return password_tag


class BackendPasswordFiles(Backend):
    """
    Implementation of the get_passwd backend
    as it was working up until 2019 - reading password files
    located in /ORA/dbs01/syscontrol/projects/systools/etc
    """
    def __init__(self, config=None, password_directory=None):
        """Initialize Backend for files.

        If no arguments are passed, cerndb-base config file is used.
        Otherwise you can either pass a Config object or a password_directory
        param. These 2 are identical:

            config = Config()
            config["getpasswd"]["password_directory"] = "/test"
            BackendPasswordFiles(config=config)
        and
            BackendPasswordFiles(password_directory="/test")



        Args:
            config (cerndb.config.Config, optional): Config object.
                Defaults to None.
            password_directory (str, optional): Directory where to look
                for password files. Defaults to None.

        Raises:
            InvalidConfigurationException: Wrong Config object
            PasswordDirectoryException: Password directory doesn't exist
        """
        settings = {"getpasswd.password_directory": password_directory}
        super(BackendPasswordFiles, self).__init__(config=config,
                                                   settings=settings)

    @classmethod
    def parse_arguments(cls, args):
        """
        Parse command-line arguments specific to this Backend
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--password_directory",
                            dest="getpasswd.password_directory")
        parser.add_argument(
            "password_tag",
            help="Password tag to retrieve")

        arguments = vars(parser.parse_args(args))

        # If password_directory not provided, try to read env
        if not arguments["getpasswd.password_directory"]:
            arguments["getpasswd.password_directory"] = \
                os.environ.get("GETPASSWD_DIRECTORY", None)
        # Remove not provided arguments, they will come from the config file
        return dict((k, v) for k, v in arguments.items() if v is not None)

    @staticmethod
    def _process_regex(data, tag):
        """
        data - password file data (str)
        tag - password tag to retrieve (str)

        Process the data with a regex, return a list of matching password tags
        """
        regex = r"^TAG {password_tag}=(.*)$"
        regex = regex.format(password_tag=tag)
        pattern = re.compile(regex, re.MULTILINE)

        matches = pattern.findall(data)
        return matches

    def validate_config(self):
        """
        Validations:
            Required keys:
                - password_directory
            - Check password_directory exists
        """
        # call parent implementation
        super(BackendPasswordFiles, self).validate_config()
        # Check that we got all the necessary information for this backend
        try:
            password_dir = Path(self.config["getpasswd"]["password_directory"])
        except KeyError:
            raise InvalidConfigurationException(
                "Missing key: password_directory")

        if not password_dir.is_dir():
            raise PasswordDirectoryException(
                f"password_directory doesn't exist: {password_dir}")

    def get(self, password_tag):
        """
        Return password for a given tag

        tag - tag to find in a password file

        returns - password if a tag was found, None if password wasn't found
        """
        # Iterate over file in the passwd directory
        passwd_dir = self.config["getpasswd"]["password_directory"]

        for passwd_file in \
                sorted(os.listdir(passwd_dir), reverse=True):
            # Only filenames starting with passwd
            if not passwd_file.startswith("passwd"):
                continue
            passwd_path = os.path.join(passwd_dir, passwd_file)
            logger.debug("Checking file: %s", passwd_path)
            try:
                with open(passwd_path) as f:
                    # read opened file
                    content = f.read()
            except IOError as e:
                if e.errno == errno.EACCES:
                    # Ignore access denied, just move to the next file
                    logger.debug("Ignoring file %s. Access denied.",
                                 passwd_path)
                    continue
                # Otherwise raise the exception
                raise IOError from e

            matching_passwords = self._process_regex(content, password_tag)
            if matching_passwords:
                # Always return the last element, if a password is redefined
                # prefer the latter one
                logger.info("password found in "
                            "PW_FILE=%s "
                            "TAG=%s USER=%s PW_DIR=%s",
                            passwd_file, password_tag,
                            getpass.getuser(),
                            passwd_dir)

                return matching_passwords[-1]

        return None


class BackendTeigi(Backend):
    """
    Backend for getting passwords from Teigi
    """
    def validate_config(self):
        """
        Validate if all necessary parameters are in the config file
        or come from command line arguments
        """
        required_keys = [
            "scope",
            "endpoint", "host_private_key_path", "host_certificate_path",
            "cern_ca_bundle_path"]
        if "getpasswd" not in self.config:
            raise InvalidConfigurationException(
                "Missing getpasswd section in the config file")
        # Check getpasswd section of the YAML
        config = self.config["getpasswd"]
        for key in required_keys:
            if key not in config:
                raise InvalidConfigurationException(
                    "Missing key: {}".format(key))
        if 'hostgroup' not in config and config['scope'] == 'hostgroup':
            raise InvalidConfigurationException(
                "Missing key: hostgroup")
        if 'service' not in config and config['scope'] == 'service':
            raise InvalidConfigurationException(
                "Missing key: hostgroup")
        if config['scope'] not in ['service', 'hostgroup', 'hosttree']:
            raise InvalidConfigurationException(
                f"Invalid scope: {config['scope']}")

    @classmethod
    def parse_arguments(cls, args):
        """
        Parse command-line arguments specific to this Backend
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "password_tag",
            help="Password tag to retrieve")
        parser.add_argument(
            "--scope",
            dest="getpasswd.scope",
            choices=["hostgroup", "service", "hosttree"],
            help="Teigi secret scope - hostgroup or service")
        parser.add_argument(
            "--hostgroup",
            dest="getpasswd.hostgroup",
            help="Hostgroup to get the password for")
        parser.add_argument(
            "--service",
            dest="getpasswd.service",
            help="Service to get the password for")
        parser.add_argument(
            "--endpoint",
            dest="getpasswd.endpoint",
            help="Full Teigi URL")
        parser.add_argument(
            "--host_private_key_path",
            dest="getpasswd.host_private_key_path",
            help="Path to host private key")
        parser.add_argument(
            "--host_certificate_path",
            dest="getpasswd.host_certificate_path",
            help="Path to host certificate")
        parser.add_argument(
            "--cern_ca_bundle_path",
            dest="getpasswd.cern_ca_bundle_path",
            help="Path to CERN CA bundle")

        arguments = vars(parser.parse_args(args))

        # Remove not provided arguments, they will come from the config file
        return dict((k, v) for k, v in arguments.items() if v is not None)

    def get(self, password_tag):
        """
        Args:
            password_tag (str): Password tag to retrieve from Teigi

        Get a tag from teigi
        """
        # First, let's format the URL, as it contains a few placeholders
        config = self.config["getpasswd"]
        scope = config["scope"]
        if scope == "hostgroup":
            hostgroup = config["hostgroup"].replace('/', '-')
            endpoint = config["endpoint"].format(
                scope=config["scope"],
                hostgroup=hostgroup,
                password_tag=password_tag)
        elif scope == "service":
            endpoint = config["endpoint"].format(
                scope=config["scope"],
                service=config["service"],
                password_tag=password_tag)
        else:
            endpoint = config["endpoint"].format(
                scope=config["scope"],
                password_tag=password_tag)

        # Call Teigi endpoint with a get request
        logger.debug("Teigi endpoint: %s", endpoint)
        result = get(
            endpoint,
            cert=(
                config['host_certificate_path'],
                config['host_private_key_path']
            ),
            allow_redirects=True,
            verify=config['cern_ca_bundle_path']
        )

        # Check status_code
        #   404 - password not found, return None
        #   200 - password found, return the password
        #   otherwise - raise an exception
        if result.status_code == 200:
            return result.json()["secret"]
        if result.status_code == 404:
            # Password for a given tag not found
            logger.debug("GET status_code: %s", result.status_code)
            return None

        raise(StatusCodeException(f"GET {endpoint},"
                                  f"status code: {result.status_code}"))
