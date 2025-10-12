#!/usr/bin/env python
"""
Script de diagnóstico para problemas en Railway
Ejecutar con: python scripts/railway_diagnostic.py
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    from django.conf import settings
    from django.db import connection
    from django.core.management import execute_from_command_line
except ImportError as e:
    print(f"❌ Error importando Django: {e}")
    sys.exit(1)

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_environment():
    print_section("VARIABLES DE ENTORNO")
    
    critical_vars = [
        'DJANGO_DEBUG', 'DJANGO_SECRET_KEY', 'DJANGO_ALLOWED_HOSTS',
        'DATABASE_URL', 'PORT'
    ]
    
    for var in critical_vars:
        value = os.environ.get(var, 'NO DEFINIDA')
        if var == 'DJANGO_SECRET_KEY' and value != 'NO DEFINIDA':
            value = f"{value[:10]}...{value[-4:]}"  # Ocultar parte de la clave
        elif var == 'DATABASE_URL' and value != 'NO DEFINIDA':
            # Ocultar contraseña en DATABASE_URL
            if '@' in value:
                parts = value.split('@')
                if len(parts) >= 2:
                    value = f"...@{parts[1]}"
        print(f"  {var}: {value}")
    
    # Verificar si DATABASE_URL usa hostname obsoleto
    database_url = os.environ.get('DATABASE_URL', '')
    if 'railway.internal' in database_url:
        print(f"  ⚠️  WARNING: DATABASE_URL usa hostname .railway.internal (obsoleto)")
    elif database_url and 'railway.app' in database_url:
        print(f"  ✅ DATABASE_URL usa hostname moderno de Railway")

def check_django_settings():
    print_section("CONFIGURACIÓN DE DJANGO")
    
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
    print(f"  SECRET_KEY configurada: {'Sí' if settings.SECRET_KEY != 'unsafe-secret-key' else 'No'}")
    
    # Configuración de seguridad
    security_settings = [
        'CSRF_COOKIE_SECURE', 'SESSION_COOKIE_SECURE', 'SECURE_SSL_REDIRECT',
        'SECURE_HSTS_SECONDS', 'SECURE_CONTENT_TYPE_NOSNIFF', 'SECURE_BROWSER_XSS_FILTER'
    ]
    
    print(f"\n  Configuración de seguridad:")
    for setting in security_settings:
        value = getattr(settings, setting, 'No configurado')
        print(f"    {setting}: {value}")

def check_database():
    print_section("CONEXIÓN A BASE DE DATOS")
    
    try:
        # Verificar configuración de base de datos
        db_config = settings.DATABASES['default']
        print(f"  Engine: {db_config['ENGINE']}")
        
        if 'HOST' in db_config:
            print(f"  Host: {db_config['HOST']}")
        if 'PORT' in db_config:
            print(f"  Port: {db_config['PORT']}")
        if 'NAME' in db_config:
            print(f"  Database: {db_config['NAME']}")
            
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print(f"  ✅ Conexión exitosa a la base de datos")
            else:
                print(f"  ❌ Error en la consulta de prueba")
                
    except Exception as e:
        print(f"  ❌ Error conectando a la base de datos: {e}")

def check_static_files():
    print_section("ARCHIVOS ESTÁTICOS")
    
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Verificar si el directorio staticfiles existe
    static_root = Path(settings.STATIC_ROOT)
    if static_root.exists():
        files_count = len(list(static_root.rglob('*')))
        print(f"  ✅ Directorio staticfiles existe con {files_count} archivos")
    else:
        print(f"  ⚠️  Directorio staticfiles no existe")

def check_installed_apps():
    print_section("APLICACIONES INSTALADAS")
    
    required_apps = ['whitenoise', 'rest_framework', 'django.contrib.staticfiles']
    missing_apps = []
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"  ✅ {app}")
        else:
            print(f"  ❌ {app} - FALTANTE")
            missing_apps.append(app)
    
    if missing_apps:
        print(f"\n  ⚠️  Aplicaciones faltantes: {missing_apps}")

def run_django_checks():
    print_section("VERIFICACIONES DE DJANGO")
    
    try:
        # Ejecutar check de Django
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('check', '--deploy', stdout=output, stderr=output)
        result = output.getvalue()
        
        if result.strip():
            print(f"  Salida del check:")
            for line in result.strip().split('\n'):
                print(f"    {line}")
        else:
            print(f"  ✅ Todas las verificaciones pasaron")
            
    except Exception as e:
        print(f"  ❌ Error ejecutando verificaciones: {e}")

def main():
    print("🚀 DIAGNÓSTICO DE RAILWAY - MEDICONECTA DJANGO")
    print(f"Directorio del proyecto: {BASE_DIR}")
    
    check_environment()
    check_django_settings()
    check_database()
    check_static_files()
    check_installed_apps()
    run_django_checks()
    
    print_section("RESUMEN")
    print("✅ Diagnóstico completado")
    print("\n📋 Próximos pasos recomendados:")
    print("1. Verificar que DATABASE_URL no use .railway.internal")
    print("2. Asegurar que DJANGO_DEBUG=0 en producción")
    print("3. Verificar que PORT esté definido por Railway")
    print("4. Revisar logs de Railway para errores específicos")

if __name__ == "__main__":
    main()
