FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy project
COPY . /app

# Create non-root user
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Ejecutar comando directo para debug
CMD ["sh", "-c", "echo '=== INICIANDO APLICACIÓN ===' && echo 'Puerto: $PORT' && echo 'Directorio: $(pwd)' && echo '=== PASO 1: MIGRACIONES ===' && python manage.py migrate --noinput && echo '✅ Migraciones completadas' && echo '=== PASO 2: STATIC FILES ===' && python manage.py collectstatic --noinput && echo '✅ Static files completados' && echo '=== PASO 3: VERIFICAR DJANGO ===' && python manage.py check --deploy && echo '✅ Django check completado' && echo '=== PASO 4: INICIAR GUNICORN ===' && exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level debug --access-logfile - --error-logfile -"]
