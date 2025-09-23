from django.db import models
from django.utils import timezone
from medicos.models import Medico
from pacientes.models import Paciente

class EstadoReserva(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    CONFIRMADA = 'confirmada', 'Confirmada'
    COMPLETADA = 'completada', 'Completada'
    CANCELADA = 'cancelada', 'Cancelada'

class Reserva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='reservas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=EstadoReserva.choices,
        default=EstadoReserva.PENDIENTE
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['fecha', 'hora_inicio']
        
    def __str__(self):
        return f"Reserva {self.paciente} con Dr. {self.medico} - {self.fecha} {self.hora_inicio}"
    
    def esta_vigente(self):
        return self.estado in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]
    
    def puede_cancelar(self):
        return self.estado in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]

class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historial')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas')
    reserva = models.OneToOneField(Reserva, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial')
    fecha = models.DateTimeField(default=timezone.now)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = "Historiales médicos"
    
    def __str__(self):
        return f"Consulta de {self.paciente} con Dr. {self.medico} - {self.fecha.strftime('%d/%m/%Y')}"

class Cobro(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='cobro')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Cobro {self.id} - ${self.monto} - {estado}"
    
    def marcar_como_pagado(self, metodo):
        self.pagado = True
        self.fecha_pago = timezone.now()
        self.metodo_pago = metodo
        self.save()