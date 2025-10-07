from django.urls import path
from . import views

app_name = 'servicios_externos'

urlpatterns = [
    # Vistas principales
    path('', views.dashboard_apis_externas, name='dashboard'),
    path('medicamentos/', views.medicamentos_view, name='medicamentos'),
    path('estadisticas-salud/', views.estadisticas_salud_view, name='estadisticas_salud'),
    path('nutricion/', views.nutricion_view, name='nutricion'),
    
    # APIs JSON
    path('api/medicamentos/', views.api_medicamentos, name='api_medicamentos'),
    path('api/estadisticas-globales/', views.api_estadisticas_globales, name='api_estadisticas_globales'),
    path('api/estadisticas-pais/', views.api_estadisticas_pais, name='api_estadisticas_pais'),
    path('api/nutricion/', views.api_nutricion, name='api_nutricion'),
]
