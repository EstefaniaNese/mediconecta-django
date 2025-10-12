#!/usr/bin/env python
"""
Script de diagnóstico específico para Railway
Ejecutar con: railway run python scripts/railway_debug.py
"""
import os
import sys
import django
from pathlib import Path

print("=== RAILWAY DEBUG SCRIPT ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    django.setup()
    print("✅ Django setup successful")
    
    from django.conf import settings
    print(f"✅ Settings loaded: DEBUG={settings.DEBUG}")
    print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Verificar base de datos
    from django.db import connection
    print("✅ Database connection module imported")
    
    # Probar conexión
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Database connection test: {result}")
    
    # Verificar tablas
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print(f"✅ Database tables: {len(tables)} tables found")
        for table in tables:
            print(f"  - {table[0]}")
    
    # Probar WSGI
    print("✅ Testing WSGI application...")
    from config.wsgi import application
    print("✅ WSGI application imported successfully")
    
    print("\n=== ALL CHECKS PASSED ===")
    print("The application should be working. Check if Gunicorn is starting correctly.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
