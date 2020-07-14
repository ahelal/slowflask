#!/bin/sh
set -eo

# Assume that clone happened in /opt/slowflask
base_dir="/opt/slowflask/"
app_user="order"
sudo apt-get update
sudo apt install -y python3-flask

if id -u "${app_user}" > /dev/null 2>&1; then
    echo "No need add ${app_user} user"
else
    sudo  useradd "${app_user}"
fi
sudo chown -R "${app_user}" "${base_dir}"

sudo cp "${base_dir}/orders/orders.service.service" /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable orders
sudo systemctl start orders
