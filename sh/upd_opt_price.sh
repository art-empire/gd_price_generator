#/usr/bin/env bash

#php /path/to/cart/admin.php -p --dispatch=advanced_import.import.import --preset_id=3

docker exec php7.4 php /app/www/admin.php -p --dispatch=import_presets_opt.import.import
