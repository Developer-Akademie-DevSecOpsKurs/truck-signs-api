#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

# Wait for the database to be up and ready, if not ready, then sleep for 5 seconds
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL not ready - sleep for 5 seconds"
  sleep 5
done

echo "PostgreSQL is active"

python manage.py collectstatic --noinput

python manage.py migrate
echo "Postgresql migrations finished"

gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8000
