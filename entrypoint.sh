#!/usr/bin/env bash
set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
RETRIES=30

echo "Waiting for postgres to connect ..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  RETRIES=$((RETRIES-1))
  if [ "$RETRIES" -le 0 ]; then
    echo "Postgres not reachable, giving up"
    exit 1
  fi
  echo "Postgres not ready yet, sleeping 5 seconds ..."
  sleep 5
done
echo "PostgreSQL is active"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
echo "Postgresql migrations finished"

# Create superuser only if it does not exist yet (idempotent)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  if python manage.py shell -c "import os, sys; from django.contrib.auth import get_user_model; sys.exit(0 if get_user_model().objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists() else 1)"; then
    echo "Superuser already exists, skipping"
  else
    python manage.py createsuperuser --noinput
    echo "Superuser created"
  fi
else
  echo "DJANGO_SUPERUSER_* not set, skipping superuser creation"
fi

exec gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8020 --workers 4