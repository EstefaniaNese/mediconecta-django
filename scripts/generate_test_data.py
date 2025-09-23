import os
import sys
import django
import random
from datetime import date, timedelta, time
from decimal import Decimal

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar modelos
from django.contrib.auth.models import User
from medicos.models import Especialidad, Medico
from pacientes.models import Paciente
from citas.models import Reserva, HistorialMedico, Cobro, EstadoReserva

def create_users_and_profiles():
    # Crear usuarios médicos
    medicos_data = [
        {
            'username': 'doctor1',
            'email': 'doctor1@example.com',
            'password': 'Doctor1@2023',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'especialidad_id': 1,
            'registro_colegio': 'MG-12345',
            'telefono': '+56912345678',
            'horario_inicio': time(8, 0),
            'horario_fin': time(17, 0),
        },
        {
            'username': 'doctor2',
            'email': 'doctor2@example.com',
            'password': 'Doctor2@2023',
            'first_name': 'Ana',
            'last_name': 'Gómez',
            'especialidad_id': 2,
            'registro_colegio': 'CA-67890',
            'telefono': '+56923456789',
            'horario_inicio': time(9, 0),
            'horario_fin': time(18, 0),
        },
        {
            'username': 'doctor3',
            'email': 'doctor3@example.com',
            'password': 'Doctor3@2023',
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'especialidad_id': 3,
            'registro_colegio': 'PE-54321',
            'telefono': '+56934567890',
            'horario_inicio': time(8, 30),
            'horario_fin': time(16, 30),
        },
    ]
    
    medicos = []
    for data in medicos_data:
        especialidad_id = data.pop('especialidad_id')
        registro_colegio = data.pop('registro_colegio')
        telefono = data.pop('telefono')
        horario_inicio = data.pop('horario_inicio')
        horario_fin = data.pop('horario_fin')
        
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults=data
        )
        
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"Usuario médico creado: {user.username}")
        
        medico, created = Medico.objects.get_or_create(
            user=user,
            defaults={
                'especialidad_id': especialidad_id,
                'registro_colegio': registro_colegio,
                'telefono': telefono,
                'horario_inicio': horario_inicio,
                'horario_fin': horario_fin,
            }
        )
        
        if created:
            print(f"Perfil de médico creado para: {user.username}")
        
        medicos.append(medico)
    
    # Crear usuarios pacientes
    pacientes_data = [
        {
            'username': 'paciente1',
            'email': 'paciente1@example.com',
            'password': 'Paciente1@2023',
            'first_name': 'María',
            'last_name': 'López',
            'rut': '12.345.678-9',
            'telefono': '+56945678901',
            'fecha_nacimiento': date(1985, 5, 15),
            'direccion': 'Av. Principal 123, Santiago',
            'grupo_sanguineo': 'O+',
            'alergias': 'Ninguna',
        },
        {
            'username': 'paciente2',
            'email': 'paciente2@example.com',
            'password': 'Paciente2@2023',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rut': '23.456.789-0',
            'telefono': '+56956789012',
            'fecha_nacimiento': date(1990, 8, 22),
            'direccion': 'Calle Secundaria 456, Valparaíso',
            'grupo_sanguineo': 'A+',
            'alergias': 'Penicilina',
        },
        {
            'username': 'paciente3',
            'email': 'paciente3@example.com',
            'password': 'Paciente3@2023',
            'first_name': 'Laura',
            'last_name': 'González',
            'rut': '34.567.890-1',
            'telefono': '+56967890123',
            'fecha_nacimiento': date(1978, 3, 10),
            'direccion': 'Pasaje Los Olivos 789, Concepción',
            'grupo_sanguineo': 'B-',
            'alergias': 'Aspirina, Mariscos',
        },
    ]
    
    pacientes = []
    for data in pacientes_data:
        rut = data.pop('rut')
        telefono = data.pop('telefono')
        fecha_nacimiento = data.pop('fecha_nacimiento')
        direccion = data.pop('direccion')
        grupo_sanguineo = data.pop('grupo_sanguineo')
        alergias = data.pop('alergias')
        
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults=data
        )
        
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"Usuario paciente creado: {user.username}")
        
        paciente, created = Paciente.objects.get_or_create(
            user=user,
            defaults={
                'rut': rut,
                'telefono': telefono,
                'fecha_nacimiento': fecha_nacimiento,
                'direccion': direccion,
                'grupo_sanguineo': grupo_sanguineo,
                'alergias': alergias,
            }
        )
        
        if created:
            print(f"Perfil de paciente creado para: {user.username}")
        
        pacientes.append(paciente)
    
    return medicos, pacientes

def create_reservas(medicos, pacientes):
    # Crear reservas
    today = date.today()
    
    # Motivos de consulta comunes
    motivos = [
        "Control de rutina",
        "Dolor de cabeza persistente",
        "Fiebre y malestar general",
        "Dolor abdominal",
        "Problemas respiratorios",
        "Revisión de exámenes",
        "Consulta por alergia",
        "Control de presión arterial",
        "Dolor muscular",
        "Problemas digestivos"
    ]
    
    # Crear reservas pasadas (completadas)
    for i in range(5):
        paciente = random.choice(pacientes)
        medico = random.choice(medicos)
        fecha = today - timedelta(days=random.randint(1, 30))
        hora_inicio = time(hour=random.randint(8, 16), minute=random.choice([0, 30]))
        hora_fin = time(hour=hora_inicio.hour + 1, minute=hora_inicio.minute)
        
        reserva = Reserva.objects.create(
            paciente=paciente,
            medico=medico,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            motivo=random.choice(motivos),
            estado=EstadoReserva.COMPLETADA
        )
        
        print(f"Reserva pasada creada: {reserva}")
        
        # Crear historial médico para esta reserva
        historial = HistorialMedico.objects.create(
            paciente=paciente,
            medico=medico,
            reserva=reserva,
            fecha=fecha,
            diagnostico=f"Diagnóstico para la consulta del {fecha}",
            tratamiento=f"Tratamiento prescrito el {fecha}",
            observaciones="Seguimiento en 2 semanas" if random.choice([True, False]) else ""
        )
        
        print(f"Historial médico creado para reserva: {reserva.id}")
        
        # Crear cobro para esta reserva
        cobro = Cobro.objects.create(
            reserva=reserva,
            monto=Decimal(random.randint(20000, 50000)),
            pagado=True,
            fecha_pago=fecha,
            metodo_pago=random.choice(["Efectivo", "Tarjeta de crédito", "Transferencia"])
        )
        
        print(f"Cobro creado para reserva: {reserva.id}")
    
    # Crear reservas futuras (pendientes o confirmadas)
    for i in range(5):
        paciente = random.choice(pacientes)
        medico = random.choice(medicos)
        fecha = today + timedelta(days=random.randint(1, 14))
        hora_inicio = time(hour=random.randint(8, 16), minute=random.choice([0, 30]))
        hora_fin = time(hour=hora_inicio.hour + 1, minute=hora_inicio.minute)
        
        reserva = Reserva.objects.create(
            paciente=paciente,
            medico=medico,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            motivo=random.choice(motivos),
            estado=random.choice([EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA])
        )
        
        print(f"Reserva futura creada: {reserva}")
        
        # Crear cobro pendiente para esta reserva
        cobro = Cobro.objects.create(
            reserva=reserva,
            monto=Decimal(random.randint(20000, 50000)),
            pagado=False
        )
        
        print(f"Cobro pendiente creado para reserva: {reserva.id}")

if __name__ == "__main__":
    print("Generando datos de prueba...")
    medicos, pacientes = create_users_and_profiles()
    create_reservas(medicos, pacientes)
    print("Datos de prueba generados con éxito!")
