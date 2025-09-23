from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("pacientes/", include("pacientes.urls")),
    path("medicos/", include("medicos.urls")),
    path("contacto/", include("contacto.urls")),
    path("citas/", include("citas.urls")),
]
