from django.urls import path

from . import views

urlpatterns = [
    path("computadora/", views.computadora, name="computadora"),
    path("computadora/deshabilitar/<int:id>", views.deleteComputadora, name="deshabilitar_computadora"),
    path("telefono/", views.telefono, name="telefono"),
    path("repuesto_computadora/", views.repuesto_computadora, name="repuestos_computadora"),
    path("repuesto_telefono/", views.repuesto_telefono, name="repuestos_telefono"),
    path("accesorio/", views.acessorio, name="accesorio"),
]