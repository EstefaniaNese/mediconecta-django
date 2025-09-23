from django.contrib import admin
from .models import Reserva, HistorialMedico, Cobro

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha', 'hora_inicio', 'estado')
    list_filter = ('estado', 'fecha', 'medico')
    search_fields = ('paciente__user__username', 'medico__user__username', 'motivo')
    date_hierarchy = 'fecha'

@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha')
    list_filter = ('fecha', 'medico')
    search_fields = ('paciente__user__username', 'medico__user__username', 'diagnostico', 'tratamiento')
    date_hierarchy = 'fecha'

@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'monto', 'pagado', 'fecha_pago')
    list_filter = ('pagado', 'fecha_pago')
    search_fields = ('reserva__paciente__user__username', 'reserva__medico__user__username')