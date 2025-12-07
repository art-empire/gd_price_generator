import logging.config
from pathlib import Path

import yaml

from settings.base import BASE_DIR

LOGGING_CONFIG = BASE_DIR / 'config' / 'logger_config.yaml'

def init_logger():

    config_file: Path = LOGGING_CONFIG

    if not config_file.exists():
        raise FileNotFoundError(f"Logging config yaml not found: {config_file}")

    with config_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
