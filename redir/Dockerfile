FROM	nginx:latest
RUN		apt-get update -y
RUN		apt-get install net-tools -y
RUN		mkdir /var/www/
RUN		mkdir /var/www/files
COPY	nginx.conf /etc/nginx/nginx.conf
CMD		["nginx", "-g", "daemon off;"]%