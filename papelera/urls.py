from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.usuarios, name="papelera_usuarios"),
    path("usuarios/habilitar/<int:id>", views.habilitar_usuarios, name="habilitar_usuarios"),
    path("usuarios/buscar/", views.buscar, name="buscar_usuario_papelera"),
]