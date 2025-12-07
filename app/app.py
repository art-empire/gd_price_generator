#!/usr/bin/env python3
import logging
import time

from price_generator import PriceGenerator
from service.print_config import print_config
from settings.logger import init_logger


logger = logging.getLogger(__name__)


def main():
    start_time = time.time()
    logger.info("Начали работу.")

    my_price_generator = PriceGenerator()
    my_price_generator.get_price()

    logger.info("Общее время работы:  %s секунд." % (time.time() - start_time))


if __name__ == "__main__":
    init_logger()
    logger.debug('start')
    print_config()
    main()
