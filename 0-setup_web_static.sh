#!/usr/bin/env bash
#Script sets up web server for deployment of web static.
sudo apt-get update
sudo apt-get install -y nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html>
<head>
</head>
<body>
Holberton School
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

if [ -L "/data/web_static/current" ]; then
	rm /data/web_static/current
fi

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
config="server {
    listen 80;
    listen [::]:80;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
}
}"
if ! grep "/hbnb_static/" /etc/nginx/sites-available/default; then
	sudo bash -c "echo '$config' >> /etc/nginx/sites-available/default"
fi
sudo service nginx restart
