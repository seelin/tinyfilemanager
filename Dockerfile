# how to build?
# docker login
## .....input your docker id and password
#docker build . -t tinyfilemanager/tinyfilemanager:master
#docker push tinyfilemanager/tinyfilemanager:master

# how to use?
# docker run -d -v /absolute/path:/var/www/html/data -p 80:80 --restart=always --name tinyfilemanager tinyfilemanager/tinyfilemanager:master

#FROM php:7.4-cli-alpine
FROM php:7.4-fpm-alpine

# if run in China
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --no-cache \
    libzip-dev \
    oniguruma-dev \
    python3 \
    py3-pip

RUN docker-php-ext-install \
    zip 
#RUN  find / -name 'nginx.conf'
#WORKDIR /var/www/html

WORKDIR /etc

COPY tinyfilemanager.php index.php
COPY tinyfilemanager.php /index.php

CMD ["sh", "-c", "php -S 0.0.0.0:80"]
