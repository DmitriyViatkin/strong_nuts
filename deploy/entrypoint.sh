#!/bin/bash
set -e

echo "==> Migrating wagtailcore..."
yes | python manage.py migrate wagtailcore

echo "==> Migrating cities_light..."
yes | python manage.py migrate cities_light

echo "==> Migrating all..."
yes | python manage.py migrate

echo "==> Collecting static..."
python manage.py collectstatic --noinput

echo "==> Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
password = '${DJANGO_SUPERUSER_PASSWORD:-admin}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser \"{username}\" created.')
else:
    print(f'Superuser \"{username}\" already exists, skipping.')
"

echo "==> Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000