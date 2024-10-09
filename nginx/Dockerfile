FROM nginx:alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    make \
    && apk add --no-cache brotli-dev \
    && mkdir /tmp/ngx_brotli \
    && cd /tmp/ngx_brotli \
    && git clone https://github.com/google/ngx_brotli.git \
    && cd ngx_brotli \
    && git submodule update --init \
    && cd /tmp \
    && git clone https://github.com/nginx/nginx.git \
    && cd nginx \
    && ./auto/configure --with-compat --add-dynamic-module=/tmp/ngx_brotli \
    && make modules \
    && cp objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/ \
    && cp objs/ngx_http_brotli_static_module.so /etc/nginx/modules/ \
    && rm -rf /tmp/* \
    && apk del .build-deps

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
