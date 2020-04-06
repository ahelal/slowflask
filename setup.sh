#!/bin/sh
set -ex

sudo apt-get update
sudo apt install -y python3-flask

if id -u slow > /dev/null 2>&1; then
    echo "No need add slow user"
else
    sudo  useradd slow
fi

sudo  chown -R slow /opt/slowflask/

sudo cp unit.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable slow
