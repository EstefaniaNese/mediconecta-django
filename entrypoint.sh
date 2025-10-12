#!/bin/bash
set -e

echo "Iniciando aplicación Django..."

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || true

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --run-syncdb || echo "Error en migraciones, continuando..."

# Crear superusuario automáticamente si las variables están configuradas
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creando superusuario..."
    python manage.py createsuperuser --noinput || true
fi

echo "Configuración completada. Iniciando servidor..."

# Ejecutar el comando pasado como argumentos (Railway usa Gunicorn)
# Si no hay argumentos, usar runserver para desarrollo local
if [ $# -eq 0 ]; then
    python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi