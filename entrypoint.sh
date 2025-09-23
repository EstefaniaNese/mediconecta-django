#!/usr/bin/env bash
set -e

# Esperar a que la base de datos esté disponible
echo "Esperando a que la base de datos esté disponible..."
python -c "
import sys
import time
import psycopg2

start_time = time.time()
timeout = 30
while True:
    try:
        psycopg2.connect(
            dbname='mediconecta',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        break
    except psycopg2.OperationalError:
        if time.time() - start_time > timeout:
            print('Tiempo de espera agotado para la conexión a la base de datos')
            sys.exit(1)
        time.sleep(1)
"
echo "Base de datos disponible!"

python manage.py collectstatic --noinput || true
python manage.py migrate

# Create a superuser automatically if DJANGO_SUPERUSER_* are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Dev server (swap with gunicorn for prod)
python manage.py runserver 0.0.0.0:8000