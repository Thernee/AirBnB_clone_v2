#!/usr/bin/env bash
# setting webservers for deployment of web_static project

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "Webstatic index page!" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/

cat <<EOL | sudo tee /etc/nginx/sites-available/default > /dev/null
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

# server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }


    location /redirect_me {
        return 301 https://twitter.com/;
    }

    error_page 404 /404.html;
    location /404 {
    	root /var/www/html;
    	internal;
    }
}
EOL

sudo service nginx restart

