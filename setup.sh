#!/bin/bash

set -e

CONFIG_FILE="settings.ini"
INSTALL_DIR="$(pwd)"

echo "🔍 Reading configuration from $CONFIG_FILE..."

# Read config values
domain=$(awk -F' *= *' '/^domain/ {print $2}' "$CONFIG_FILE")
book_dir=$(awk -F' *= *' '/^book_dir/ {print $2}' "$CONFIG_FILE")

echo "📦 Installing system dependencies (nginx, python3, pip)..."
sudo dnf install -y python3 python3-pip nginx

echo "🐍 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "📁 Ensuring books directory exists at: $book_dir"
mkdir -p "$book_dir"

echo "🌐 Configuring nginx for domain: $domain"
NGINX_CONF="/etc/nginx/conf.d/bookbit.conf"
if [ ! -f "$NGINX_CONF" ] || ! grep -q "$domain" "$NGINX_CONF"; then
  cat <<EOF | sudo tee "$NGINX_CONF"
server {
    listen 80;
    server_name $domain;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
else
  echo "✅ nginx config already exists and is up to date."
fi

echo "🛠️ Setting up systemd service..."
SYSTEMD_UNIT="/etc/systemd/system/bookbit.service"
if [ ! -f "$SYSTEMD_UNIT" ]; then
  cat <<EOF | sudo tee "$SYSTEMD_UNIT"
[Unit]
Description=Bookbit EPUB server
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/run.py
WorkingDirectory=$INSTALL_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF
else
  echo "✅ systemd unit file already exists."
fi

echo "🔁 Reloading and starting services..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable bookbit
sudo systemctl restart bookbit
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "✅ Bookbit is now installed and running!"
echo "🌐 Access it at: http://$domain"
