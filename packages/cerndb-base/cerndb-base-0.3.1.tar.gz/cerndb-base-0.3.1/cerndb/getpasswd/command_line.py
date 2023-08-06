"""
Command line script for get_passwd
"""
# pylint: disable=redefined-builtin
from sys import stdout, exit
import json
import argparse

from cerndb.getpasswd.backends import BackendPasswordFiles, BackendTeigi, \
    InvalidConfigurationException, PasswordDirectoryException
from cerndb.log import logger, setup_root_logger

from cerndb.config import CFG


def parse_arguments():
    """
    Pass command line argument for choosing the backend
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--backend",
        help="Backend, the default one reads password files",
        dest="getpasswd.backend",
        choices=["files", "teigi"])
    parser.add_argument(
        "--help", "-h",
        help="Display help and exit",
        action="store_true")
    parser.add_argument("--debug", action="store_const",
                        dest="log.level",
                        help="Log level for the Console logger",
                        const="DEBUG")
    parser.add_argument("--verbose", action="store_const",
                        dest="log.level",
                        help="Log level for the Console logger",
                        const="DEBUG")

    # Parse only known, the rest will be parsed in the Backend impl
    known_args, remaining = parser.parse_known_args()
    # Display help from here if no --backend, otherwise, display help from
    # the appropriate backend!
    if known_args.help:
        if getattr(known_args, 'getpasswd.backend'):
            remaining.append("--help")
        else:
            parser.print_help()
            exit(0)
    else:
        known_args.help = None
    # Remove not provided arguments, they will come from the config file
    known_args = dict((k, v) for k, v in vars(known_args).items()
                      if v is not None)
    return (known_args, remaining)


def main():
    """
    This function is invoked by the get_passwd script
    """
    args, remaining = parse_arguments()
    CFG.set_args(args)
    setup_root_logger(CFG, tag="getpasswd.command_line")
    #################################################################
    # Select Backend
    # Read backend from command line, fall back to the config file
    try:
        config = CFG["getpasswd"]
    except KeyError:
        logger.error("Config file %s missing getpasswd section.",
                     CFG.used_file)
        exit(1)

    backend_name = args.get("backend", config.get("backend", None))

    if not backend_name:
        logger.error("Default backend not found in the config file! "
                     "(it can be also specified via --backend)")
        exit(1)

    if backend_name == "files":
        logger.debug("Using PasswordFiles Backend")
        backend_class = BackendPasswordFiles
    elif backend_name == "teigi":
        logger.debug("Using Teigi Backend")
        backend_class = BackendTeigi
    else:
        logger.error("Not supported Backend: %s", backend_name)
        exit(1)
    #################################################################
    # Parse args of a Backend
    arguments = backend_class.parse_arguments(remaining)

    # Create configuration - command line + config file
    CFG.set_args(arguments)

    logger.debug(
        "Used config (config file + command line args): %s",
        json.dumps(config, indent=4, sort_keys=True))
    # Create backend object
    try:
        backend = backend_class(config=CFG)
    except InvalidConfigurationException as exc:
        logger.error("Invalid config file: %s", exc)
        exit(1)
    except PasswordDirectoryException as exc:
        logger.error(exc)
        exit(1)

    password = backend.get(arguments["password_tag"])
    # If password was found - print it
    if password:
        stdout.write(password)
    else:
        # Otherwise exit with 1
        exit(1)


if __name__ == '__main__':
    main()
