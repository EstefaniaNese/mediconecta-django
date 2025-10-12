FROM python:3.12-slim

# System deps (gcc for psycopg2, tzdata, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential curl tzdata libpq-dev &&         rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set Python to not buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Copy project
COPY . /app

# Create non-root user (optional)
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
ENV PORT=8000
CMD ["/bin/bash", "entrypoint.sh"]