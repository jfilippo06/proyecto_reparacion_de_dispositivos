from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.usuarios, name="papelera_usuario"),
    path("usuarios/habilitar/<int:id>", views.habilitar_usuarios, name="habilitar_usuario"),
    path("inventario/computadora/", views.computadora, name="papelera_computadora"),
    path("inventario/habilitar/<int:id>", views.habilitar_computadoras, name="habilitar_computadora"),
    path("inventario/telefono/", views.telefono, name="papelera_telefono"),
    path("inventario/telefono/<int:id>", views.habilitar_telefonos, name="habilitar_telefono"),
    path("inventario/repuesto_computadora/", views.repuesto_computadora, name="papelera_repuesto_computadora"),
    path("inventario/repuesto_computadora/<int:id>", views.habilitar_repuesto_computadora, name="habilitar_repuesto_computadora"),
]