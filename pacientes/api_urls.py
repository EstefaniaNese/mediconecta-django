from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PacienteViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')

urlpatterns = [
    path('api/', include(router.urls)),
]
