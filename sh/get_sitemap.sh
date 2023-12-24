#/usr/bin/env bash

docker exec php7.4 php /app/www/admin.php --dispatch=xmlsitemap.generate
