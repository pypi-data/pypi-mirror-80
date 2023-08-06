"""Test logging library"""
import logging
from cerndb.config import Config
from cerndb.log import setup_root_logger, logger


def test_custom_logger():
    """Test setting a custom logger"""
    # Asser default level
    assert logger.level == logging.INFO  # nosec
    # Change level with Config object
    config = Config()
    config["log"]["level"] = "DEBUG"
    setup_root_logger(config=config, tag="TAG")
    assert logger.level == logging.DEBUG  # nosec
    # Updating config with set_args updates logger
    config.set_args({"log.level": "WARNING"})
    assert logger.level == logging.WARNING  # nosec
