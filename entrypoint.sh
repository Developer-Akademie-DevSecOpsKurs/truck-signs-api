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

exec "$@"