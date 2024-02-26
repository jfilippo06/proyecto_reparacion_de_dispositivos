from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.users, name="usuarios"),
    path("usuarios/actualizar/<int:id>", views.updateUsers, name="actualizar_usuarios"),
    path("usuarios/deshabilitar/<int:id>", views.deleteUsers, name="deshabilitar_usuarios"),
    path("usuarios/cancelar/", views.cancelar, name="cancelar_usuarios"),
    path("usuarios/buscar/", views.buscar, name="buscar_usuario"),
    path("impuestos/", views.impuesto, name="impuesto"),
    path("impuestos/activar_impuesto/", views.activar_impuesto, name="activar_impuesto"),
    path("impuestos/desactivar_impuesto/", views.desactivar_impuesto, name="desactivar_impuesto"),
    path("impuestos/actualizar_impuesto/", views.actualizar_impuesto, name="actualizar_impuesto"),
    path("dolar/", views.dolar, name="dolar"),
    path("dolar/activar_dolar/", views.activar_dolar, name="activar_dolar"),
    path("dolar/desactivar_dolar/", views.desactivar_dolar, name="desactivar_dolar"),
    path("dolar/actualizar_dolar/", views.actualizar_dolar, name="actualizar_dolar"),
]