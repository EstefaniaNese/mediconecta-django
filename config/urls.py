from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def favicon_view(request):
    """Manejo simple para favicon.ico"""
    return HttpResponse("", content_type="image/x-icon")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("pacientes/", include("pacientes.urls")),
    path("medicos/", include("medicos.urls")),
    path("contacto/", include("contacto.urls")),
    path("citas/", include("citas.urls")),
    path("servicios-externos/", include("servicios_externos.urls")),
    # APIs REST
    path("medicos/", include("medicos.api_urls")),
    path("pacientes/", include("pacientes.api_urls")),
    # API de Autenticación
    path("api/auth/", include("accounts.api_urls")),
    # Favicon
    path("favicon.ico", favicon_view, name="favicon"),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
