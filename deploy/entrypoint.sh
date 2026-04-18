#!/bin/bash
set -e

echo "==> Migrating wagtailcore..."
yes | python manage.py migrate wagtailcore

echo "==> Migrating all..."
yes | python manage.py migrate

echo "==> Collecting static..."
python manage.py collectstatic --noinput

echo "==> Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000