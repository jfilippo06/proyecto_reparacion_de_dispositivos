from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.users, name="usuarios"),
    path("usuarios/actualizar/<int:id>", views.updateUsers, name="actualizar_usuarios"),
    path("usuarios/deshabilitar/<int:id>", views.deleteUsers, name="deshabilitar_usuarios"),
]