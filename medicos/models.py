from django.db import models
from django.contrib.auth.models import User

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Especialidades"

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="medico")
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, related_name="medicos")
    registro_colegio = models.CharField(max_length=60, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fin = models.TimeField(null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username