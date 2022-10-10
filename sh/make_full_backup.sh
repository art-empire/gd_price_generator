#/usr/bin/env bash

#php /path/to/cart/admin.php -p --dispatch=advanced_import.import.import --preset_id=3

docker exec -it php7.4 php /app/www/admin.php -p --dispatch=datakeeper.backup --backup_database=Y --backup_files=Y --dbdump_schema=Y --dbdump_data=Y --dbdump_tables=all --extra_folders[0]=var/files --extra_folders[1]=var/attachments --extra_folders[2]=var/langs
