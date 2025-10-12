"""
Comando para listar todos los usuarios del sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Lista todos los usuarios del sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Mostrar solo usuarios activos'
        )
        parser.add_argument(
            '--superusers-only',
            action='store_true',
            help='Mostrar solo superusuarios'
        )

    def handle(self, *args, **options):
        users = User.objects.all()
        
        # Filtros
        if options['active_only']:
            users = users.filter(is_active=True)
        if options['superusers_only']:
            users = users.filter(is_superuser=True)
        
        users = users.order_by('-date_joined')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No hay usuarios en el sistema'))
            return
        
        self.stdout.write(self.style.MIGRATE_HEADING(f'\n=== Usuarios del Sistema ({users.count()}) ===\n'))
        
        for user in users:
            status = []
            if user.is_superuser:
                status.append('SUPER')
            if user.is_staff:
                status.append('STAFF')
            if not user.is_active:
                status.append('INACTIVO')
            
            status_str = f' [{", ".join(status)}]' if status else ''
            
            self.stdout.write(
                f'{user.id:4d}  {user.username:20s}  {user.email:30s}  '
                f'{user.first_name} {user.last_name}{status_str}'
            )
        
        self.stdout.write('\n')

