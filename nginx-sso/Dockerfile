# From https://raw.githubusercontent.com/flavienbwk/nginx-keycloak/main/Dockerfile

FROM openresty/openresty:1.19.9.1-5-alpine-fat

RUN mkdir /var/log/nginx
RUN cp /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.pem

RUN apk update && apk add --no-cache bash openssl-dev git gcc gettext
RUN luarocks install lua-resty-openidc
