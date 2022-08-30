#/usr/bin/env bash

docker exec -it php7.4 php /app/www/admin.php --dispatch=xmlsitemap.generate
