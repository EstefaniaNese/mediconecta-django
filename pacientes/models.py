from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="paciente")
    rut = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    grupo_sanguineo = models.CharField(max_length=10, blank=True)
    alergias = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username