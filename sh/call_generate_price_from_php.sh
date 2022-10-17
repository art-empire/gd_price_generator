#!/bin/bash

echo "generate price"

PATH=$(pwd)

# echo $PATH

/usr/bin/python3 $PATH/gd_price_generator/gd_price_generator.py

echo "generate price end"
