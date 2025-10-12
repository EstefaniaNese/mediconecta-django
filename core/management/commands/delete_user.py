"""
Comando para eliminar usuarios desde la línea de comandos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Elimina un usuario por username o email'

    def add_arguments(self, parser):
        parser.add_argument(
            'identifier',
            type=str,
            help='Username o email del usuario a eliminar'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma la eliminación sin preguntar'
        )

    def handle(self, *args, **options):
        identifier = options['identifier']
        confirm = options['confirm']
        
        # Buscar usuario por username o email
        user = None
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Usuario no encontrado: {identifier}')
                )
                return
        
        # Mostrar información del usuario
        self.stdout.write(f'\nUsuario encontrado:')
        self.stdout.write(f'  ID: {user.id}')
        self.stdout.write(f'  Username: {user.username}')
        self.stdout.write(f'  Email: {user.email}')
        self.stdout.write(f'  Nombre: {user.first_name} {user.last_name}')
        self.stdout.write(f'  Superusuario: {user.is_superuser}')
        self.stdout.write(f'  Staff: {user.is_staff}')
        self.stdout.write(f'  Activo: {user.is_active}')
        self.stdout.write(f'  Fecha de registro: {user.date_joined}')
        
        # Confirmar eliminación
        if not confirm:
            confirmation = input('\n¿Estás seguro de eliminar este usuario? (sí/no): ')
            if confirmation.lower() not in ['sí', 'si', 'yes', 's', 'y']:
                self.stdout.write(self.style.WARNING('✗ Eliminación cancelada'))
                return
        
        # Eliminar usuario
        username = user.username
        user.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Usuario "{username}" eliminado exitosamente')
        )

