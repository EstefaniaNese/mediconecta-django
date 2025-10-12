#!/bin/bash
set -e

echo "=== INICIANDO APLICACIÓN ==="
echo "Puerto: $PORT"
echo "Directorio: $(pwd)"

echo "=== PASO 1: MIGRACIONES ==="
python manage.py migrate --noinput
echo "✅ Migraciones completadas"

echo "=== PASO 2: STATIC FILES ==="
python manage.py collectstatic --noinput
echo "✅ Static files completados"

echo "=== PASO 3: VERIFICAR DJANGO ==="
python manage.py check --deploy
echo "✅ Django check completado"

echo "=== PASO 4: INICIAR GUNICORN ==="
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
