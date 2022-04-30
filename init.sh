#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

gunicorn --bind :8000 app:flask_app --reload 2> ./log/log.txt # あとでログ消す