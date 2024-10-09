FROM nginx:alpine

RUN apk add --no-cache \
    git \
    gcc \
    libc-dev \
    make \
    zlib-dev \
    pcre-dev \
    openssl-dev \
    linux-headers \
    curl \
    gnupg \
    libxslt-dev \
    gd-dev


RUN git clone https://github.com/google/ngx_brotli.git /tmp/ngx_brotli && \
    cd /tmp/ngx_brotli && \
    git submodule update --init && \
    cd /tmp && \
    wget http://nginx.org/download/nginx-1.21.6.tar.gz && \
    tar -xzvf nginx-1.21.6.tar.gz && \
    cd nginx-1.21.6 && \
    ./configure --with-compat --add-dynamic-module=../ngx_brotli && \
    make modules && \
    cp objs/*.so /etc/nginx/modules/


RUN echo "load_module modules/ngx_http_brotli_filter_module.so;" >> /etc/nginx/nginx.conf && \
    echo "load_module modules/ngx_http_brotli_static_module.so;" >> /etc/nginx/nginx.conf


COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
