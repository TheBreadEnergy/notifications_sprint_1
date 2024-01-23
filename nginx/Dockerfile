FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY config /etc/nginx/conf.d/

EXPOSE 80

EXPOSE 81

EXPOSE 8080


