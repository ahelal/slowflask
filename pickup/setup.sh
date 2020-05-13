#!/bin/sh
set -euo pipefail

# Assume that clone happened in /opt/slowflask
base_dir="/opt/slowflask/"
slow_user="slow"

sudo apt-get update
sudo apt install -y python3-flask

if id -u "${slow_user}" > /dev/null 2>&1; then
    echo "No need add ${slow_user} user"
else
    sudo  useradd "${slow_user}"
fi
sudo chown -R "${slow_user}" "${base_dir}"

sudo cp "${base_dir}/pickup/slow.service" /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable slow
sudo systemctl start slow
