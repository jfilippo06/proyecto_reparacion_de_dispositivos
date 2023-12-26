from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.usuarios, name="papelera_usuario"),
    path("usuarios/habilitar/<int:id>", views.habilitar_usuarios, name="habilitar_usuario"),
    path("inventario/computadora/", views.computadora, name="papelera_computadora"),
    path("inventario/habilitar/<int:id>", views.habilitar_computadoras, name="habilitar_computadora"),
]