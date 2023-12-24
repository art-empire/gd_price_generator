#!/bin/bash

echo "generate price"



PATH=$(pwd)

echo $PATH

/bin/ls -lah $PATH/gd_price_generator/

$PATH/gd_price_generator/sh/remove_old_files.sh

# source $PATH/gd_price_generator/.venv/bin/activate


# /usr/bin/python3 -m venv $PATH/gd_price_generator/.venvphp

# source $PATH/gd_price_generator/.venvphp/bin/activate

#PYTHONIOENCODING=utf8 pip3 freeze

#PYTHONIOENCODING=utf8 python3 ../gd_price_generator.py

# /usr/bin/pip install -r $PATH/gd_price_generator/requirements.txt


echo "--//--"

/usr/bin/python3 $PATH/gd_price_generator/gd_price_generator.py

echo "--//--"

echo "generate price end"
