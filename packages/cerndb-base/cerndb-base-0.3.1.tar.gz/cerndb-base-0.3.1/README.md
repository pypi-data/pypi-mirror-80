`python3-cerndb` is a Python package that provides commonly used Python3 functionalities for the group. Examples are logging and managing configuration files.

[[_TOC_]]

# Installation

* with `pip`
    ```
    python3 -m pip install cerndb
    ```
* as RPM
    ```
    yum install python3-cerndb
    ```

# Basic usage

Quickstart:

```python
from argparse import ArgumentParser
from cerndb.config import CFG
from cerndb.log import logger

parser = ArgumentParser()
parser.add_argument('--debug', action="store_const",
                    dest="log.level", const="DEBUG")
parser.add_argument('--parameter')
args = parser.parse_args()

# Override default config file
# to change logging level if --debug was passed to the script
# logger is automatically reinitialized with the new level
CFG.set_args(args)

# Log something - goes to console and /var/log/cerndb.log
logger.info("Config file I read from: %s", CFG.used_file)

# If --parameter passed print the value, otherwise KeyError raised
print(CFG["parameter"])

# You can manually override
CFG["parameter"] = "my new value"
```

> The Quickstart assumes, you don't have a custom config file for your application. If you do, [use the Config object instead of CFG.](#custom-config-file-with-logging-parameters)

# Logging

> **cerndb.log** module.

Python logging module. (By default) it logs messages to console and to `/var/log/cerndb.log`. It uses `INFO` level. To use it, just import the module:


```python
from cerndb.log import logger
```

> `logger` is a Python logging object,

You can emit messages the usual way:
```python
logger.info("info message")
logger.error("error message")
# etc.
```

#### Default Logging configuration

By default the logger logs to:
- the console
- `/var/log/cerndb.log` file. **Important:** this file needs proper permissions: `0666`.

Default attributes are the following.

```yaml
log:
  level: "INFO"
  file: "/var/log/cerndb.log"
  fmt: '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s'
  datefmt: '%d/%b/%Y:%H:%M:%S %z'
```

In the table below *dot* means a nested YAML dictionary.

| Attribute | Default value | Description |
| --- | --- | --- |
| `log.level` | `INFO` | Logging level |
| `log.file` | `/var/log/cerndb.log` | Log file to use |
| `log.fmt` | `[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s` | Format of the log message |
| `log.datefmt` | `%d/%b/%Y:%H:%M:%S %z` | Format of the date in logs |

### Logging-related config file options

Default values to configure the logger are read from a config file that is present in one of the following locations (first-found is read):
* `${PWD}/cerndb/config.yaml`
* `~/cerndb/config.yaml`
* `/etc/cerndb/config.yaml`
* module installation path (Python `site-library`)

**If no configuration file is present** in any of the locations, default fallback values hardcoded in the code will be used. See the default values in the table above. A fallback value will also be used for any key not present in the config file.

### Changing logging message level

> The default level is **INFO**

Allowed logging levels are available in the upstream documentation:
https://docs.python.org/3/howto/logging.html#logging-levels

You can programmatically change the level by calling `logger.setLevel([DESIRED_LEVEL])` at any time after importing the module. A level can be a string, like `"INFO"`, `"DEBUG"` or a `logging` constant, like `logging.INFO` (then you must import `logging`).

```python
from cerndb.log import logger

logger.setLevel("DEBUG")
```

### Overriding logging defaults with command-line arguments

To override the default logger settings (like the message level) you need to properly name your command-line `argparse` arguments using a *dot notation*, like `log.level`. See available attributes in [this table](#default-logging-configuration). Then, use `config.set_args()` of `cerndb.config` module. Have a look at the example below:

```python
from argparse import ArgumentParser
from cerndb.config import CFG
from cerndb.log import logger

parser = ArgumentParser()
parser.add_argument('--debug', action="store_const",
                    dest="log.level", const="DEBUG")
args = parser.parse_args()

# Override default config file values and re-initialize the logger
CFG.set_args(args)
```

*DEBUG* will replace the default *INFO* value.

Use the snippet above if you don't have a separate config file for your application, otherwise read [Custom config file with logging parameters](#custom-config-file-with-logging-parameters).


### Custom config file with logging parameters

If you would like to have a [custom config file](#config-class) for your application, you can either rely on default options or provide `log` config keys in your config file. `cerndb.log` logger uses by default a default `cerndb` config object. You can change that with a call to `setup_root_logger`. The snippet to reinitialize the logger is the following:

```python
from cerndb.config import Config
from cerndb.log import logger, setup_root_logger

config = Config(module_name="syscontrol")
# Has to be called, otherwise settings from CFG are used:
setup_root_logger(config)
```

If you don't provide one of the [keys](#default-logging-configuration), the logger will use a hardcoded default value.

# Config

> **cerndb.config** module.

This is a module to manage the configuration of your application.

### Basic usage

The snippet below will search the following locations, looking for a file named `config.yaml`. If the file is found, no further locations are searched:
- `${PWD}/my_module/`
- `~/my_module/`
- `/etc/my_module/`
- `[PYTHON_SITE_LIBRARY]/my_module`

```python
from cerndb.config import Config

config = Config(module_name="my_module")
# Accessing parameters:
print(config["my_param"])
# Nested parameters
print(config["log"]["level"])
```

### Config class

`Config` class is used to load the configuration data and to manipulate it. You can easily override config file values with command line options (like `--debug`) [using set_args](#command-line-attributes). Those features make `cerndb.config` ideal for storing all of your application configuration data.

`Config` constructor accepts a few parameters to parametrize loading the config.

By default, the `Config()` tries to open a file named `config.yaml` in a couple of predefined locations.


```python
Config(
  module_name="",
  search_paths=None,
  filename="config.yaml")
```

#### Attributes

* `module_name` - name that will be appended to paths used to search for the config file. For example, with `module_name=test`, `~/test` would be searched instead of `~/`
* `search_paths` - an array of paths to search for the config file. It will override the default ones.
* `filename` - name of the config file to look for. Default: `config.yaml`

#### Default search locations

- `${PWD}/`
- `~/`
- `/etc/`
- `[PYTHON_SITE_LIBRARY]/`

#### Example

```python
from cerndb.config import Config

config = Config(module_name="myapp")
```

### Default cerndb config - CFG

When importing `cerndb.config`, you get access to a `Config` object named `CFG`. This object holds the default configuration parameters that are distributed along with the Python code or with Puppet. The location of this config file on disk is next to the module - in Python `site-library`.

```python
from cerndb.config import CFG
```

This default configuration holds for now the default logging settings. In the future more settings will be added.

You can use both, the custom file and you own application config file (import both - `from cerndb.config import Config, CFG`).


### Command-line attributes

You can easily override config file values with command line attributes that come from `argparse`. `set_args` method is provided for that.
To override nested YAML values, used the *dot* notation (see example).
Basically, you need to use the `dest` attribute of `ArgumentParser` `add_argument` method.

The signature is the following:

`set_args(argparse.Namespace)`

Example:
```python
from argparse import ArgumentParser
from cerndb.config import Config

config = Config(module_name="myapp")

parser = ArgumentParser()
parser.add_argument('--debug', action="store_const",
                    dest="log.level", const="DEBUG")
parser.add_argument('--url',
                    dest="connection.url")
args = parser.parse_args()

config.set_args(args)
```

> You can also overwrite the default config values - `CFG.set_args(args)`

#### Using dot notation

Dot notation is used to override nested yaml structures. Example:

YAML config file:
```yaml
connection:
  properties:
    name: "test"
```
Use the following `dest=` attribute, so the value of `--name` overwrites the default:
```python
import argparse

parser = ArgumentParser()
parser.add_argument('--name', dest="connection.properties.name")

# then config.set_args(args) as shown above
```

### Reading attributes

An object of `Config` class behaves like a Python `dict`. So, constructs like these are possible:
```python
# First, create the object: config = Config()
config["log"]["level"]
# manually set new value
config["log"]["level"] = "DEBUG"

with open(config["file_path"]) as f:
    # read the file
    pass
```

### Which config file has been used?

Any config file object has an attribute `used_file` that allows to easily see which config file was actually read.

Example:
```python
config = Config()
print(config.used_file)

# Exemplary output: '/home/development/python3-cerndb/cerndb/cerndb/config.yaml'
```

If no config file has been found:
- `used_file` is set to `None`
- `Config` object is an empty dictionary

# get_passwd

## get_passwd script

`get_passwd` allows to choose from 2 backends - **password files** or **teigi** with `--backend` argument.

```
get_passwd --help
usage: get_passwd [--backend {files,teigi}] [--help] [--debug] [--verbose]

optional arguments:
  --backend {files,teigi}
                        Backend, the default one reads password files
  --help, -h            Display help and exit
  --debug               Log level for the Console logger
  --verbose             Log level for the Console logger
```

After choosing a backend, help can be displayed for each of them, for example, `get_passwd --backend files --help`
```
usage: get_passwd [-h] [--password_directory GETPASSWD.PASSWORD_DIRECTORY]
                  password_tag

positional arguments:
  password_tag          Password tag to retrieve

optional arguments:
  -h, --help            show this help message and exit
  --password_directory GETPASSWD.PASSWORD_DIRECTORY
```

Default values are read from the config file.

## Python module

### BackendPasswordFiles

To read from password files, use the following snippet. All default settings are take from cerndb-base config file.

```python
from cerndb.getpasswd.backends import BackendPasswordFiles
backend = BackendPasswordFiles()
password = backend.get('passwd_user_sysctl')
```

* `backend.get()` returns **None** if password wasn't found in any of the files
* constructor accepts a custom password directory `BackendPasswordFiles(password_directory="/tmp/passwords")`
* `cerndb.config.Config` object can be passed to the constructor: `BackendPasswordFiles(config=Config())`

### BackendTeigi

Read directly from Teigi.

```python
from cerndb.getpasswd.backends import BackendTeigi
backend = BackendTeigi()
password = backend.get('passwd_user_sysctl')
```

* To replace default values of the config file, pass a `cerndb.config.Config` object: `backend = BackendPasswordFiles(config=Config())`
  * for example:
    ```python
    config = Config()
    config["getpasswd"]["hostgroup"] = "appserver"
    backend = BackendPasswordFiles(config=config)
    ```

### Migrating from systools

#### Migrating from `GetPasswd` class

In `cerndb-infra-systools`:
```python
from systools.get_passwd import GetPasswd
getpasswd = GetPasswd()
password = getpasswd.get('tag')
```

**New way:**
```python
from cerndb.getpasswd.backends import BackendPasswordFiles
backend = BackendPasswordFiles()
password = backend.get('tag')
```

#### Migrating from `systools.config_manager`

```python
from systools.config_manager import get_config, NoConfigFileException, \
    IncorrectConfigFileException
 config = get_config([etc_dir,
                      '/ORA/dbs01/syscontrol/projects/vegas-cli/etc'],
                      'config', 'VEGAS_CLI_CONFIGFILE')
json_path = config.get('common', 'default_json_path_query')
```

New way:
* first change config file to use YAML format
* ```python
  from cerndb.config import Config
  config = Config(module_name="vegas")
  json_path = config["default_json_path_query"]
  ```

## Configurable parameters

Below are listed all configurable parameters. Required params are in **bold**.
Default config file is installed with this package. It's also distributed with Puppet and stored in `/etc/cerndb/config/config.yaml`

All parameters listed below can be overridden with command-line arguments. For example, to override `host_certificate_path`, use `--host_certificate_path`

#### `common`
- **backend** - default backend to user
#### `files` backend
- **password_directory** - directory where the password files are

#### `Teigi` backend
- **teigi_scope** - default scope [default=hostgroup] (supported - `hostgroup`, `service`)
- **teigi_url** - teigi endpoint
- **host_certificate_path** - path to host certificate
- **host_private_key_path** - path to host certificate

Example of a config file:

```yaml
getpasswd:
  #############################################
  # Common
  #############################################
  backend: files
  #############################################
  # Files backend
  #############################################
  password_directory: /ORA/dbs01/syscontrol/projects/systools/etc/
  #############################################
  # Teigi backend
  #############################################
  hostgroup: dia
  service: dia
  scope: hostgroup
  endpoint: https://woger.cern.ch:8202/tbag/v2/{scope}/{hostgroup}/secret/{password_tag}/
  host_private_key_path: /var/lib/puppet/ssl/private_keys/{hostname}.pem
  host_certificate_path: /var/lib/puppet/ssl/certs/{hostname}.pem
  cern_ca_bundle_path: /etc/ssl/certs/CERN-bundle.pem
```


# Examples

> A script with examples of usage of this python package is distributed and can be found in `/usr/bin/cerndb_example`

## Custom config file

Let's assume we have the following config file stored in `/etc/myapp/myconf.yaml`:
```yaml
logger:
  level: INFO
json: /etc/myjson.json
```

We can read the config file like:
```python
from cerndb.config import Config

config = Config(module_name="myapp", filename="myconf.yaml")
```
> *Note, that you could rely on the default filename `config.yaml` and avoid specifying `filename="myconf.yaml"`*

Then assume, we can change the logger level by providing a `--debug` flag to our script. The same goes to changing the `json` location.

```python
from argparse import ArgumentParser
from cerndb.config import Config
from cerndb.log import logger

config = Config(module_name="myapp", filename="myconf.yaml")

parser = ArgumentParser()
parser.add_argument('--debug', action="store_const",
                    dest="log.level", const="DEBUG")
parser.add_argument('--json')
args = parser.parse_args()

# The important bit:
config.set_args(args)

# will print "DEBUG" if --debug provided
print(config["log"]["level"])

# Will print the message
logger.debug("A debug message")
```
