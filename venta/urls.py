from django.urls import path
from . import views

urlpatterns = [
    path('consultar_cliente/', views.client, name='cliente'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('cancelar/', views.cancelar, name='cancelar'),
    path('facturar_cliente/', views.facturar_cliente, name='facturar_cliente'),
    path('agregar_articulo/<int:id>', views.agregar_articulo, name='agregar_articulo'),
]