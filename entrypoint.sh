#!/bin/bash
set -e

echo "Iniciando aplicación Django..."

# Verificar variables de entorno críticas
echo "Verificando configuración..."
echo "DEBUG: $DJANGO_DEBUG"
echo "ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"
echo "DATABASE_URL presente: $([ -n "$DATABASE_URL" ] && echo "Sí" || echo "No")"

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || echo "Advertencia: Error en collectstatic"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --run-syncdb || {
    echo "Error en migraciones, intentando con --fake-initial..."
    python manage.py migrate --fake-initial || echo "Error crítico en migraciones"
    exit 1
}

# Crear superusuario automáticamente si las variables están configuradas
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creando superusuario..."
    python manage.py createsuperuser --noinput || true
fi

echo "Configuración completada. Iniciando servidor..."

# Verificar que Django puede iniciar correctamente
echo "Verificando que Django puede iniciar..."
python manage.py check --deploy || {
    echo "Error en verificación de Django"
    exit 1
}

# Ejecutar el comando pasado como argumentos (Railway usa Gunicorn)
# Si no hay argumentos, usar runserver para desarrollo local
if [ $# -eq 0 ]; then
    python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi