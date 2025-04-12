#!/bin/sh

set -e

STORAGE_DIR="./storage"

echo "Ensuring storage directory exists at $STORAGE_DIR..."
mkdir -p "$STORAGE_DIR"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Checking for superuser '$DJANGO_SUPERUSER_USERNAME'..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() else exit(1)"; then
    echo "Superuser '$DJANGO_SUPERUSER_USERNAME' already exists. Skipping creation."
else
    python manage.py createsuperuser
    echo "Superuser '$DJANGO_SUPERUSER_USERNAME' creation process finished."
fi
