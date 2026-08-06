#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

# Wait for the database to be up and ready, if not ready, then sleep for 5 seconds
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL not ready - sleep for 5 seconds"
  sleep 5
done

echo "PostgreSQL is active"

python src/manage.py collectstatic --noinput

python src/manage.py migrate
echo "Postgresql migrations finished"


echo "creating superuser"
python src/manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    # Korrekter Aufruf: username hier übergeben
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

gunicorn --chdir src tsa_app.wsgi:application --bind 0.0.0.0:8000
