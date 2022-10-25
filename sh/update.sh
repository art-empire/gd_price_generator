#!/bin/bash

cd ~/gooood/app/www/gd_price_generator/sh

#./make_db_backup.sh
./call_generate_price.sh
./upd_main_price.sh
./upd_opt_price.sh
./get_sitemap.sh
./warm_up_cache.sh
