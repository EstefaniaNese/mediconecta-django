from django.contrib import admin
from .models import Medico, Especialidad

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'especialidad', 'registro_colegio', 'disponible')
    list_filter = ('especialidad', 'disponible')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'registro_colegio')