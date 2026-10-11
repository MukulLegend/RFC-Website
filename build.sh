#!/usr/bin/env bash
# Runs on Render at every deploy.
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Creates your admin login the first time (needs DJANGO_SUPERUSER_* variables); ignored if it exists.
python manage.py createsuperuser --noinput || true
