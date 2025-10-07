import requests
import json
from django.conf import settings
from django.core.cache import cache
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MedicamentosService:
    """
    Servicio para consumir la API de medicamentos de OpenFDA
    """
    
    BASE_URL = "https://api.fda.gov/drug/label.json"
    
    @classmethod
    def buscar_medicamento(cls, nombre: str, limit: int = 10) -> Dict:
        """
        Busca información sobre medicamentos por nombre
        """
        cache_key = f"medicamento_{nombre}_{limit}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        try:
            params = {
                'search': f'openfda.brand_name:"{nombre}"',
                'limit': limit
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Procesar los resultados
            medicamentos = []
            for result in data.get('results', []):
                medicamento = {
                    'nombre': result.get('openfda', {}).get('brand_name', ['Desconocido'])[0] if result.get('openfda', {}).get('brand_name') else 'Desconocido',
                    'principio_activo': result.get('openfda', {}).get('substance_name', ['Desconocido'])[0] if result.get('openfda', {}).get('substance_name') else 'Desconocido',
                    'fabricante': result.get('openfda', {}).get('manufacturer_name', ['Desconocido'])[0] if result.get('openfda', {}).get('manufacturer_name') else 'Desconocido',
                    'descripcion': result.get('description', ['Sin descripción'])[0] if result.get('description') else 'Sin descripción',
                    'indicaciones': result.get('indications_and_usage', ['Sin indicaciones'])[0] if result.get('indications_and_usage') else 'Sin indicaciones',
                    'efectos_secundarios': result.get('warnings', ['Sin información'])[0] if result.get('warnings') else 'Sin información'
                }
                medicamentos.append(medicamento)
            
            result = {
                'total': data.get('meta', {}).get('results', {}).get('total', 0),
                'medicamentos': medicamentos
            }
            
            # Cachear por 1 hora
            cache.set(cache_key, result, 3600)
            return result
            
        except requests.RequestException as e:
            logger.error(f"Error al consultar API de medicamentos: {e}")
            return {
                'error': 'No se pudo conectar con el servicio de medicamentos',
                'total': 0,
                'medicamentos': []
            }
        except Exception as e:
            logger.error(f"Error inesperado en búsqueda de medicamentos: {e}")
            return {
                'error': 'Error interno del servidor',
                'total': 0,
                'medicamentos': []
            }

class EnfermedadesService:
    """
    Servicio para consumir información sobre enfermedades desde una API pública
    """
    
    BASE_URL = "https://disease.sh/v3/covid-19"
    
    @classmethod
    def obtener_estadisticas_globales(cls) -> Dict:
        """
        Obtiene estadísticas globales de COVID-19 (como ejemplo de API médica)
        """
        cache_key = "covid_global_stats"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        try:
            response = requests.get(f"{cls.BASE_URL}/all", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'casos_totales': data.get('cases', 0),
                'casos_activos': data.get('active', 0),
                'recuperados': data.get('recovered', 0),
                'fallecidos': data.get('deaths', 0),
                'casos_criticos': data.get('critical', 0),
                'casos_hoy': data.get('todayCases', 0),
                'fallecidos_hoy': data.get('todayDeaths', 0),
                'recuperados_hoy': data.get('todayRecovered', 0),
                'poblacion_afectada': data.get('population', 0),
                'ultima_actualizacion': data.get('updated', 0)
            }
            
            # Cachear por 30 minutos
            cache.set(cache_key, result, 1800)
            return result
            
        except requests.RequestException as e:
            logger.error(f"Error al consultar API de enfermedades: {e}")
            return {
                'error': 'No se pudo conectar con el servicio de estadísticas médicas',
                'casos_totales': 0,
                'casos_activos': 0,
                'recuperados': 0,
                'fallecidos': 0
            }
        except Exception as e:
            logger.error(f"Error inesperado en estadísticas de enfermedades: {e}")
            return {
                'error': 'Error interno del servidor',
                'casos_totales': 0,
                'casos_activos': 0,
                'recuperados': 0,
                'fallecidos': 0
            }
    
    @classmethod
    def obtener_estadisticas_por_pais(cls, pais: str = "Chile") -> Dict:
        """
        Obtiene estadísticas de COVID-19 por país
        """
        cache_key = f"covid_stats_{pais}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        try:
            response = requests.get(f"{cls.BASE_URL}/countries/{pais}", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'pais': data.get('country', pais),
                'casos_totales': data.get('cases', 0),
                'casos_activos': data.get('active', 0),
                'recuperados': data.get('recovered', 0),
                'fallecidos': data.get('deaths', 0),
                'casos_criticos': data.get('critical', 0),
                'casos_por_millon': data.get('casesPerOneMillion', 0),
                'fallecidos_por_millon': data.get('deathsPerOneMillion', 0),
                'poblacion': data.get('population', 0),
                'ultima_actualizacion': data.get('updated', 0)
            }
            
            # Cachear por 30 minutos
            cache.set(cache_key, result, 1800)
            return result
            
        except requests.RequestException as e:
            logger.error(f"Error al consultar API de estadísticas por país: {e}")
            return {
                'error': f'No se pudo obtener estadísticas para {pais}',
                'pais': pais,
                'casos_totales': 0,
                'casos_activos': 0,
                'recuperados': 0,
                'fallecidos': 0
            }
        except Exception as e:
            logger.error(f"Error inesperado en estadísticas por país: {e}")
            return {
                'error': 'Error interno del servidor',
                'pais': pais,
                'casos_totales': 0,
                'casos_activos': 0,
                'recuperados': 0,
                'fallecidos': 0
            }

class NutricionService:
    """
    Servicio para consumir información nutricional
    """
    
    BASE_URL = "https://api.edamam.com/api/nutrition-data"
    
    @classmethod
    def obtener_informacion_nutricional(cls, alimento: str) -> Dict:
        # Para este ejemplo, retornamos datos simulados ya que la API real requiere autenticación
        alimentos_nutricion = {
            'manzana': {
                'nombre': 'Manzana',
                'calorias': 52,
                'proteinas': 0.3,
                'carbohidratos': 14,
                'fibra': 2.4,
                'azucar': 10.4,
                'grasas': 0.2,
                'vitamina_c': 4.6,
                'potasio': 107
            },
            'platano': {
                'nombre': 'Plátano',
                'calorias': 89,
                'proteinas': 1.1,
                'carbohidratos': 23,
                'fibra': 2.6,
                'azucar': 12,
                'grasas': 0.3,
                'vitamina_c': 8.7,
                'potasio': 358
            },
            'naranja': {
                'nombre': 'Naranja',
                'calorias': 47,
                'proteinas': 0.9,
                'carbohidratos': 12,
                'fibra': 2.4,
                'azucar': 9,
                'grasas': 0.1,
                'vitamina_c': 53.2,
                'potasio': 181
            }
        }
        
        alimento_lower = alimento.lower()
        if alimento_lower in alimentos_nutricion:
            return alimentos_nutricion[alimento_lower]
        else:
            return {
                'error': f'Información nutricional no disponible para {alimento}',
                'sugerencias': list(alimentos_nutricion.keys())
            }
