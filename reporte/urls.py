from django.urls import path
from . import views

urlpatterns = [
    path('recibo/', views.recibo, name='recibo'),
    path('reparaciones/', views.reporteRepaciones, name='reporte_reparaciones'),
    path('clientes/', views.reporteCliente, name='reporte_cliente'),
    path('inventario/', views.reporteInventario, name='reporte_inventario'),
    path('ventas/', views.reporteVenta, name='reporte_venta'),
]