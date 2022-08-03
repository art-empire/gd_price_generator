#!/usr/bin/env python3

import time

from src.main import PriceGenerator

start_time = time.time()
print('Начали работу.')

my_price_generator = PriceGenerator()
my_price_generator.get_price()

print('Общее время работы:  %s секунд.' % (time.time() - start_time))
