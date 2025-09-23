from django.urls import path
from . import views

app_name = "citas"
urlpatterns = [
    path("reservas/", views.reserva_lista, name="reserva_lista"),
    path("reservas/crear/", views.reserva_crear, name="reserva_crear"),
    path("reservas/<int:pk>/", views.reserva_detalle, name="reserva_detalle"),
    path("reservas/<int:pk>/cancelar/", views.reserva_cancelar, name="reserva_cancelar"),
    path("reservas/<int:reserva_pk>/historial/crear/", views.historial_crear, name="historial_crear"),
    path("reservas/<int:reserva_pk>/cobro/actualizar/", views.cobro_actualizar, name="cobro_actualizar"),
    path("reservas/<int:reserva_pk>/cobro/pagar/", views.cobro_pagar, name="cobro_pagar"),
]
