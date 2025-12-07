import logging
import pprint

from settings.config import get_config, Config

logger = logging.getLogger(__name__)

def print_config():

    config: Config = get_config()

    logger.debug('Текущий конфиг:')

    for line in  pprint.pformat(config.model_dump()).splitlines():
        logger.debug(f'\033[37;1m{line}\033[0m')