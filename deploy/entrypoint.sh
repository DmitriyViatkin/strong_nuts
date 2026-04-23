#!/bin/bash
set -e

echo "==> Waiting for database..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT', 5432),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        dbname=os.environ.get('POSTGRES_DB'),
    )
    sys.exit(0)
except Exception as e:
    print(f'DB not ready: {e}')
    sys.exit(1)
" 2>&1; do
  echo "Waiting 3 seconds..."
  sleep 3
done
echo "==> Database is ready!"

echo "==> Migrating (pass 1, ignoring errors)..."
python manage.py migrate --noinput 2>&1 || true

echo "==> Syncing translation fields (pass 1)..."
yes | python manage.py sync_page_translation_fields 2>&1 || true

echo "==> Migrating (pass 2)..."
python manage.py migrate --noinput 2>&1 || true

echo "==> Syncing translation fields (pass 2)..."
yes | python manage.py sync_page_translation_fields 2>&1 || true

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