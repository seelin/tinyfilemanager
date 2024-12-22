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
    py3-pip \
    nginx

RUN docker-php-ext-install zip 

WORKDIR /var/www/html

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY default.conf /etc/nginx/http.d/default.conf
COPY tinyfilemanager.php index.php
COPY rindex.py ./
COPY startd.sh ./
EXPOSE 80 82 85
RUN ./startd.sh

#CMD ["/bin/sh","./startd.sh"]

CMD [ "python3", "./rindex.py" ]

#COPY tinyfilemanager.php /index.php

#CMD ["sh", "-c", "php -S 0.0.0.0:80"]
#CMD ["nginx"]
