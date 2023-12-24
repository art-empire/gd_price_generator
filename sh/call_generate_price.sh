#!/bin/bash

echo "generate price"


# PATH=$(pwd)

# echo $PATH

./remove_old_files.sh

source ../.venv/bin/activate

PYTHONIOENCODING=utf8 python3 ../gd_price_generator.py

echo "generate price end"
