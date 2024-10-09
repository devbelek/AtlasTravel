FROM nginx:alpine

# Установка модулей Brotli и Gzip
RUN apk add --no-cache nginx-mod-brotli

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Активируем Brotli модуль
RUN echo "load_module modules/ngx_http_brotli_filter_module.so;" >> /etc/nginx/nginx.conf && \
    echo "load_module modules/ngx_http_brotli_static_module.so;" >> /etc/nginx/nginx.conf

EXPOSE 80
