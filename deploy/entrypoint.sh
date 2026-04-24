#!/bin/bash
# НЕ set -e тут — керуємо помилками вручну
echo "NEW ENTRYPOINT"

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

echo "==> Making missing migrations..."
python manage.py makemigrations --noinput 2>&1 || true

# Обходимо wagtail_modeltranslation через окремий settings без нього
echo "==> Migrating wagtailcore directly (bypassing wagtail_modeltranslation)..."
DJANGO_SETTINGS_MODULE=config.settings.base python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

# Патчимо INSTALLED_APPS — прибираємо wagtail_modeltranslation тимчасово
import django.conf
apps = list(django.conf.settings.INSTALLED_APPS)
if 'wagtail_modeltranslation' in apps:
    apps.remove('wagtail_modeltranslation')
django.conf.settings.INSTALLED_APPS = apps

django.setup()
from django.core.management import call_command
call_command('migrate', 'contenttypes', '--noinput', verbosity=1)
call_command('migrate', 'auth', '--noinput', verbosity=1)
call_command('migrate', 'wagtailcore', '--noinput', verbosity=1)
call_command('migrate', 'cities_light', '--noinput', verbosity=1)
" 2>&1 || true

echo "==> Migrating all apps (pass 1)..."
python manage.py migrate --noinput 2>&1 || true

echo "==> Syncing translation fields (pass 1)..."
yes | python manage.py sync_page_translation_fields 2>&1 || true

echo "==> Migrating all apps (pass 2)..."
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