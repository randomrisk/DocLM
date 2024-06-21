FROM nginx:1.19.8-alpine

ENV TZ=Asia/Shanghai

RUN sed -i "s@http://dl-cdn.alpinelinux.org/@https://repo.huaweicloud.com/@g" /etc/apk/repositories \
    && apk update \
    && apk add curl busybox-extras --no-cache \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" >  /etc/timezone \
    && rm -rf /var/cache/apk/*

WORKDIR /work

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY MP_verify_piMy6UNXEL5kJVZs.txt /work/MP_verify_piMy6UNXEL5kJVZs.txt

CMD ["nginx","-g","daemon off;"]