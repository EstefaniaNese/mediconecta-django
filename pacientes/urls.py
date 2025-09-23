from django.urls import path
from . import views
app_name = "pacientes"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
