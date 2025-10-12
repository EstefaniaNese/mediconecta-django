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

# Simple CMD - Railway will override with startCommand
CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]
