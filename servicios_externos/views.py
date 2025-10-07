from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services import MedicamentosService, EnfermedadesService, NutricionService
import json

@login_required
def dashboard_apis_externas(request):
    """
    Dashboard principal para mostrar información de APIs externas
    """
    return render(request, 'servicios_externos/dashboard.html')

@login_required
def medicamentos_view(request):
    """
    Vista para buscar y mostrar información de medicamentos
    """
    medicamentos = []
    error = None
    
    if request.method == 'POST':
        nombre_medicamento = request.POST.get('nombre_medicamento', '').strip()
        if nombre_medicamento:
            resultado = MedicamentosService.buscar_medicamento(nombre_medicamento)
            if 'error' in resultado:
                error = resultado['error']
            else:
                medicamentos = resultado.get('medicamentos', [])
    
    return render(request, 'servicios_externos/medicamentos.html', {
        'medicamentos': medicamentos,
        'error': error
    })

@login_required
def estadisticas_salud_view(request):
    """
    Vista para mostrar estadísticas de salud globales y por país
    """
    # Obtener estadísticas globales
    stats_globales = EnfermedadesService.obtener_estadisticas_globales()
    
    # Obtener estadísticas de Chile
    stats_chile = EnfermedadesService.obtener_estadisticas_por_pais('Chile')
    
    return render(request, 'servicios_externos/estadisticas_salud.html', {
        'stats_globales': stats_globales,
        'stats_chile': stats_chile
    })

@login_required
def nutricion_view(request):
    """
    Vista para consultar información nutricional
    """
    info_nutricional = None
    error = None
    
    if request.method == 'POST':
        alimento = request.POST.get('alimento', '').strip()
        if alimento:
            info_nutricional = NutricionService.obtener_informacion_nutricional(alimento)
            if 'error' in info_nutricional:
                error = info_nutricional['error']
    
    return render(request, 'servicios_externos/nutricion.html', {
        'info_nutricional': info_nutricional,
        'error': error
    })

# APIs JSON para AJAX
@login_required
@require_http_methods(["GET"])
def api_medicamentos(request):
    """
    API JSON para buscar medicamentos
    """
    nombre = request.GET.get('nombre', '').strip()
    if not nombre:
        return JsonResponse({'error': 'Nombre de medicamento requerido'}, status=400)
    
    resultado = MedicamentosService.buscar_medicamento(nombre)
    return JsonResponse(resultado)

@login_required
@require_http_methods(["GET"])
def api_estadisticas_globales(request):
    """
    API JSON para obtener estadísticas globales
    """
    resultado = EnfermedadesService.obtener_estadisticas_globales()
    return JsonResponse(resultado)

@login_required
@require_http_methods(["GET"])
def api_estadisticas_pais(request):
    """
    API JSON para obtener estadísticas por país
    """
    pais = request.GET.get('pais', 'Chile')
    resultado = EnfermedadesService.obtener_estadisticas_por_pais(pais)
    return JsonResponse(resultado)

@login_required
@require_http_methods(["GET"])
def api_nutricion(request):
    """
    API JSON para obtener información nutricional
    """
    alimento = request.GET.get('alimento', '').strip()
    if not alimento:
        return JsonResponse({'error': 'Nombre de alimento requerido'}, status=400)
    
    resultado = NutricionService.obtener_informacion_nutricional(alimento)
    return JsonResponse(resultado)