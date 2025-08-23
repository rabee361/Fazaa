FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
RUN apt-get update && apt-get install -y certbot python3-certbot-nginx

COPY nginx.conf /etc/nginx/conf.d