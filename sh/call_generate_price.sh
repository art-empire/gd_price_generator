#!/bin/bash

echo "generate price"

# PATH=$(pwd)

# echo $PATH

source ../.venv/bin/activate

python3 ..//gd_price_generator.py

echo "generate price end"
