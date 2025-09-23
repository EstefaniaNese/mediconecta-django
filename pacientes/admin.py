from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rut', 'telefono', 'fecha_nacimiento')
    list_filter = ('fecha_nacimiento',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'rut', 'telefono')