"""Test cerndb config."""
from cerndb.config import Config, CFG


def test_default_config():
    """Test default config file is correctly read."""
    config = Config()
    assert config["getpasswd"]["password_directory"] == \
        "/ORA/dbs01/syscontrol/projects/systools/etc"


def test_cfg_contains_default():
    """CFG object should contain default values."""
    assert CFG["log"]["level"] == "INFO"
    assert CFG["getpasswd"]["password_directory"] == \
        "/ORA/dbs01/syscontrol/projects/systools/etc"
    assert isinstance(CFG, Config)


def test_config_initialize_with_dict():
    """Initialize Config object with a dict."""
    con = Config(data={"test": "data"})
    assert con["test"] == "data"
