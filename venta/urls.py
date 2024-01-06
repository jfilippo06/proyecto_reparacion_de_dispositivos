from django.urls import path
from . import views

urlpatterns = [
    path('consultar_cliente/', views.client, name='cliente'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('facturar_cliente/', views.facturar_cliente, name='facturar_cliente'),
]