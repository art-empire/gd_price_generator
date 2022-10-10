#/usr/bin/env bash

#php /path/to/cart/admin.php -p --dispatch=advanced_import.import.import --preset_id=3

docker exec -it php7.4 php /app/www/admin.php -p --dispatch=datakeeper.backup --backup_database=Y --backup_files=N --dbdump_schema=Y --dbdump_data=Y --dbdump_tables=all