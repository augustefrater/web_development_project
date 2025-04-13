#!/bin/sh

echo "🔧 Entering /app directory..."
cd /app || exit 1

echo "📦 Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "👤 Creating superuser if it doesn't exist..."
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
" | python manage.py shell

echo "🚀 Running command: $@"
exec "$@"
