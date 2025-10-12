"""
Comando de diagnóstico para verificar el estado de la aplicación en producción
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model
from django.conf import settings
import sys

User = get_user_model()

class Command(BaseCommand):
    help = 'Verifica el estado de la configuración de producción'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Diagnóstico de Producción ===\n'))
        
        all_checks_passed = True
        
        # 1. Verificar conexión a base de datos
        self.stdout.write(self.style.MIGRATE_LABEL('1. Verificando conexión a base de datos...'))
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('   ✓ Conexión a base de datos exitosa'))
                
                # Mostrar info de la base de datos
                db_settings = settings.DATABASES['default']
                self.stdout.write(f"   Motor: {db_settings['ENGINE']}")
                if 'NAME' in db_settings:
                    self.stdout.write(f"   Base de datos: {db_settings.get('NAME', 'N/A')}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error en conexión: {str(e)}'))
            all_checks_passed = False
        
        # 2. Verificar tablas de autenticación
        self.stdout.write(self.style.MIGRATE_LABEL('\n2. Verificando tablas de autenticación...'))
        try:
            user_count = User.objects.count()
            self.stdout.write(self.style.SUCCESS(f'   ✓ Tabla de usuarios existe ({user_count} usuarios)'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error en tabla de usuarios: {str(e)}'))
            all_checks_passed = False
        
        # 3. Verificar migraciones pendientes
        self.stdout.write(self.style.MIGRATE_LABEL('\n3. Verificando migraciones...'))
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            targets = executor.loader.graph.leaf_nodes()
            plan = executor.migration_plan(targets)
            
            if plan:
                self.stdout.write(self.style.WARNING(f'   ⚠ Hay {len(plan)} migraciones pendientes:'))
                for migration in plan:
                    self.stdout.write(f'     - {migration[0].app_label}.{migration[0].name}')
                all_checks_passed = False
            else:
                self.stdout.write(self.style.SUCCESS('   ✓ Todas las migraciones están aplicadas'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error verificando migraciones: {str(e)}'))
            all_checks_passed = False
        
        # 4. Verificar configuración de seguridad
        self.stdout.write(self.style.MIGRATE_LABEL('\n4. Verificando configuración de seguridad...'))
        self.stdout.write(f'   DEBUG: {settings.DEBUG}')
        self.stdout.write(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
            self.stdout.write(f'   CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}')
        else:
            self.stdout.write(self.style.WARNING('   ⚠ CSRF_TRUSTED_ORIGINS no está configurado'))
            all_checks_passed = False
        
        # 5. Verificar configuración de sesiones
        self.stdout.write(self.style.MIGRATE_LABEL('\n5. Verificando configuración de sesiones...'))
        self.stdout.write(f'   SESSION_COOKIE_SECURE: {getattr(settings, "SESSION_COOKIE_SECURE", "No configurado")}')
        self.stdout.write(f'   CSRF_COOKIE_SECURE: {getattr(settings, "CSRF_COOKIE_SECURE", "No configurado")}')
        
        # Resumen final
        self.stdout.write('\n' + '='*50)
        if all_checks_passed:
            self.stdout.write(self.style.SUCCESS('\n✓ TODOS LOS CHECKS PASARON EXITOSAMENTE'))
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR('\n✗ ALGUNOS CHECKS FALLARON - REVISAR ARRIBA'))
            sys.exit(1)

