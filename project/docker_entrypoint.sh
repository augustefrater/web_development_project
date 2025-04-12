#!/bin/sh

echo "🔧 Entrando a /app..."
cd /app || exit 1

echo "📦 Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "👤 Creando superusuario si no existe..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
      User.objects.filter(username='admin').exists() or \
      User.objects.create_superuser('admin', 'admin@localhost', 'admin')" \
      | python manage.py shell

echo "🚀 Arrancando servidor Django..."
python manage.py runserver 0.0.0.0:8000