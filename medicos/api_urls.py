from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MedicoViewSet, EspecialidadViewSet

router = DefaultRouter()
router.register(r'medicos', MedicoViewSet, basename='medico')
router.register(r'especialidades', EspecialidadViewSet, basename='especialidad')

urlpatterns = [
    path('api/', include(router.urls)),
]
