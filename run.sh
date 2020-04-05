#!/bin/sh
set -ex

python3 ./main.py >> /tmp/flask.log 2>&1  &
