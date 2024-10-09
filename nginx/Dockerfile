FROM nginx:alpine

# Установка необходимых зависимостей для сборки
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    make \
    git \
    brotli-dev \
    && mkdir -p /usr/src \
    && cd /usr/src \
    && git clone --recurse-submodules https://github.com/google/ngx_brotli.git \
    && cd /usr/src/ngx_brotli \
    && git submodule update --init --recursive \
    && cd /usr/src \
    && git clone https://github.com/nginx/nginx.git \
    && cd nginx \
    && ./auto/configure --with-compat --add-dynamic-module=/usr/src/ngx_brotli \
    && make modules \
    && cp objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/ \
    && cp objs/ngx_http_brotli_static_module.so /etc/nginx/modules/ \
    && rm -rf /usr/src \
    && apk del .build-deps

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Активируем Brotli модули
RUN echo "load_module /etc/nginx/modules/ngx_http_brotli_filter_module.so;" >> /etc/nginx/nginx.conf \
    && echo "load_module /etc/nginx/modules/ngx_http_brotli_static_module.so;" >> /etc/nginx/nginx.conf

EXPOSE 80
