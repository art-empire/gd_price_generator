#!/bin/bash

#php /path/to/cart/admin.php -p --dispatch=advanced_import.import.import --preset_id=3

echo '======='
time docker exec -t php7.4 php /app/www/admin.php -p --dispatch=datakeeper.backup --backup_database=Y --backup_files=N --dbdump_schema=Y --dbdump_data=Y --dbdump_tables=all
date
echo '======='
