from django.urls import path

from . import views

urlpatterns = [
    path("computadora/", views.inventario_computadora, name="inventario_computadora"),
    path("telefono/", views.inventario_telefono, name="inventario_telefono"),
    path("repuesto_computadora/", views.inventario_repuesto_computadora, name="inventario_repuestos_computadora"),
    path("repuesto_telefono/", views.inventario_repuesto_telefono, name="inventario_repuestos_telefono"),
    path("accesorio/", views.inventario_acessorio, name="inventario_accesorio"),
]