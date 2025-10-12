#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la conexión a la base de datos en Railway.
Ejecutar en Railway con: railway run python scripts/check_railway_db.py
"""

import os
import sys

def check_database_config():
    """Verifica la configuración de la base de datos"""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE CONFIGURACIÓN DE BASE DE DATOS")
    print("=" * 60)
    print()
    
    # 1. Verificar si DATABASE_URL existe
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: Variable DATABASE_URL no encontrada")
        print()
        print("Solución:")
        print("1. Ve a Railway Dashboard → tu servicio → Variables")
        print("2. Asegúrate de que PostgreSQL esté vinculado")
        print("3. Ver RAILWAY_DATABASE_FIX.md para más detalles")
        return False
    
    print("✓ Variable DATABASE_URL encontrada")
    print()
    
    # 2. Verificar formato de la URL
    print("📋 Análisis de DATABASE_URL:")
    print("-" * 60)
    
    # Extraer componentes (sin mostrar la contraseña completa)
    try:
        # Formato: postgresql://user:password@host:port/database
        if '@' in database_url:
            credentials, rest = database_url.split('@', 1)
            protocol_user = credentials.split('://', 1)
            
            if len(protocol_user) == 2:
                protocol = protocol_user[0]
                user = protocol_user[1].split(':')[0]
                
                host_port_db = rest.split('/', 1)
                host_port = host_port_db[0]
                database = host_port_db[1] if len(host_port_db) > 1 else 'N/A'
                
                print(f"Protocolo: {protocol}://")
                print(f"Usuario: {user}")
                print(f"Host: {host_port}")
                print(f"Base de datos: {database}")
                print()
                
                # 3. Verificar hostname obsoleto
                if 'railway.internal' in host_port:
                    print("❌ PROBLEMA DETECTADO: Hostname obsoleto")
                    print(f"   Hostname actual: {host_port}")
                    print()
                    print("🔧 SOLUCIÓN:")
                    print("   1. Ve a RAILWAY_DATABASE_FIX.md")
                    print("   2. Sigue los pasos para actualizar DATABASE_URL")
                    print("   3. El hostname debe ser: XXXX.railway.app:PUERTO")
                    print()
                    return False
                elif 'railway.app' in host_port:
                    print("✓ Hostname moderno detectado (correcto)")
                else:
                    print(f"⚠️  Hostname inesperado: {host_port}")
                    print("   (Puede ser correcto si usas otro proveedor)")
        
    except Exception as e:
        print(f"⚠️  No se pudo analizar la URL (formato inesperado)")
        print(f"   Error: {e}")
        print()
    
    # 4. Intentar conectar
    print()
    print("🔌 Intentando conectar a la base de datos...")
    print("-" * 60)
    
    try:
        # Configurar Django
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        from django.db import connection
        
        # Intentar conectar
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✓ Conexión exitosa")
            print(f"✓ PostgreSQL version: {version[0]}")
            print()
            
            # Verificar tablas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            print(f"✓ Número de tablas en la base de datos: {table_count}")
            
            if table_count == 0:
                print()
                print("⚠️  No hay tablas en la base de datos")
                print("   Ejecuta: python manage.py migrate")
            
        print()
        print("=" * 60)
        print("✅ DIAGNÓSTICO COMPLETADO: Configuración correcta")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ ERROR al conectar: {e}")
        print()
        print("🔧 POSIBLES CAUSAS:")
        print("   1. Hostname .railway.internal obsoleto")
        print("   2. Credenciales incorrectas")
        print("   3. PostgreSQL no está ejecutándose")
        print("   4. Firewall/red bloqueando la conexión")
        print()
        print("📖 Ver RAILWAY_DATABASE_FIX.md para soluciones")
        print()
        return False

if __name__ == '__main__':
    success = check_database_config()
    sys.exit(0 if success else 1)

