#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

# Wait for the database to be up and ready, if not ready, then sleep for 5 seconds
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  echo "If not ready, waiting 5 seconds"
  sleep 5
done

echo "PostgreSQL is active"

python manage.py collectstatic --noinput

python manage.py migrate
echo "Postgresql migrations finished"

if python manage.py shell -c "
import sys
from django.contrib.auth import get_user_model
sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)
"; then
  echo "User: superuser found"
else
  python manage.py createsuperuser --noinput
  echo "User created"
fi


gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8000
