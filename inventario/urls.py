from django.urls import path

from . import views

urlpatterns = [
    path("computadora/", views.computadora, name="computadora"),
    path("computadora/deshabilitar/<int:id>", views.deleteComputadora, name="deshabilitar_computadora"),
    path("computadora/actualizar/<int:id>", views.updateComputadora, name="actualizar_computadora"),
    path("telefono/", views.telefono, name="telefono"),
    path("telefono/deshabilitar/<int:id>", views.deleteTelefono, name="deshabilitar_telefono"),
    path("telefono/actualizar/<int:id>", views.updateTelefono, name="actualizar_telefono"),
    path("repuesto_computadora/", views.repuesto_computadora, name="repuestos_computadora"),
    path("repuesto_telefono/", views.repuesto_telefono, name="repuestos_telefono"),
    path("accesorio/", views.acessorio, name="accesorio"),
]