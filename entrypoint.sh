#!/bin/sh

echo "⏳ Aguardando banco de dados..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "✅ Banco de dados disponível"

echo "🔄 Aplicando migrations..."
python manage.py migrate --noinput

echo "👤 Verificando superuser..."

python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superuser criado")
    else:
        print("ℹ️ Superuser já existe")
else:
    print("⚠️ Variáveis de superuser não definidas")
END

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando servidor..."
exec "$@"