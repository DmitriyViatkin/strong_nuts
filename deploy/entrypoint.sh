#!/bin/bash
set -e

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
email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
password = '${DJANGO_SUPERUSER_PASSWORD:-admin}'
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print(f'Superuser \"{email}\" created.')
else:
    print(f'Superuser \"{email}\" already exists, skipping.')
"

echo "==> Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000