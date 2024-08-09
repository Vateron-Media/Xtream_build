# Build binaries file

## Index

* [Preassembly](#preassembly)
* [NGINX](#nginx-binary)
* [NGINX-rtmp](#nginx-rtmp-binary)
* [php-fpm](#php-fpm-binary)


## Preassembly
```
sudo apt-get install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxml2 libxml2-dev uuid-dev
```


Download source openssl
``` 
wget https://github.com/openssl/openssl/releases/download/openssl-3.3.1/openssl-3.3.1.tar.gz
```
Unzip the file
```
tar -xzvf openssl-3.3.1.tar.gz
```

## nginx binary
Download source
```
wget  https://nginx.org/download/nginx-1.26.1.tar.gz
```

```
tar -zxvf nginx-1.26.1.tar.gz
```

```
cd nginx-1.26.1
```

Configure binaries
```
./configure --prefix=/home/xtreamcodes/nginx/ --http-client-body-temp-path=/home/xtreamcodes/tmp/client_temp --http-proxy-temp-path=/home/xtreamcodes/tmp/proxy_temp --http-fastcgi-temp-path=/home/xtreamcodes/tmp/fastcgi_temp --lock-path=/home/xtreamcodes/tmp/nginx.lock --http-uwsgi-temp-path=/home/xtreamcodes/tmp/uwsgi_temp --http-scgi-temp-path=/home/xtreamcodes/tmp/scgi_temp --conf-path=/home/xtreamcodes/nginx/conf/nginx.conf --error-log-path=/home/xtreamcodes/logs/error.log --http-log-path=/home/xtreamcodes/logs/access.log --pid-path=/home/xtreamcodes/nginx/nginx.pid --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_v2_module --with-ld-opt='-Wl,-z,relro -Wl,--as-needed -static' --with-pcre --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-threads --with-mail --with-mail_ssl_module --with-file-aio --with-cpu-opt=generic --with-cc-opt='-static -static-libgcc -g -O2 -Wformat -Wall' --with-openssl=/root/openssl-3.3.1
```

Build binaries
```
make
```

Print version
```
/root/nginx-1.26.1/objs/nginx -V
```


## nginx-rtmp binary
Download source
```
wget https://github.com/arut/nginx-rtmp-module/archive/refs/tags/v1.2.2.tar.gz
```

```
tar -xzvf v1.2.2.tar.gz
```

```
cd nginx-1.26.1
```

Configure binaries
```
./configure --prefix=/home/xtreamcodes/nginx_rtmp/ --lock-path=/home/xtreamcodes/nginx_rtmp/nginx_rtmp.lock --conf-path=/home/xtreamcodes/nginx_rtmp/conf/nginx.conf --error-log-path=/home/xtreamcodes/logs/rtmp_error.log --http-log-path=/home/xtreamcodes/logs/rtmp_access.log --pid-path=/home/xtreamcodes/nginx_rtmp/nginx.pid --add-module=/root/nginx-rtmp-module-1.2.2 --with-ld-opt='-Wl,-z,relro -Wl,--as-needed -static' --with-pcre --without-http_rewrite_module --with-file-aio --with-ipv6 --with-cpu-opt=generic --with-cc-opt='-static -static-libgcc -g -O2 -Wformat -Wall' --with-openssl=/root/openssl-3.3.1
```

Build binaries
```
make
```

Print version
```
/root/nginx-1.26.1/objs/nginx -v
```

## php-fpm binary
Install package 
```
sudo apt-get install libcurl4-gnutls-dev libbz2-dev libzip-dev
```
Download source
```
wget -O php-7.3.25.tar.gz http://php.net/get/php-7.3.25.tar.gz/from/this/mirror
```

```
tar -xzvf php-7.3.25.tar.gz
```

```
cd php-7.3.25
```

Configure binaries
```
./configure  --prefix=/home/xtreamcodes/php --with-zlib-dir --enable-mbstring --enable-calendar --with-curl --with-gd --disable-rpath --enable-inline-optimization --with-bz2 --with-zlib --enable-sockets --enable-sysvsem --enable-sysvshm --enable-pcntl --enable-mbregex --enable-exif --enable-bcmath --with-mhash --enable-zip --with-pcre-regex --with-pdo-mysql=mysqlnd --with-mysqli=mysqlnd --with-openssl --with-fpm-user=xtreamcodes --with-fpm-group=xtreamcodes --with-libdir=/lib/x86_64-linux-gnu --with-gettext --with-xmlrpc --with-xsl --enable-opcache --enable-fpm --enable-libxml --enable-static --disable-shared --with-mcrypt
```

Build binaries
```
make
```

Out file path
```
/root/php-7.3.25/sapi/fpm/php-fpm
```