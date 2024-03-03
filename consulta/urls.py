from django.urls import path
from . import views

urlpatterns = [
    path('consultar_inventario/', views.consultar_inventario, name='consultar_inventario'),
    path('consultar_reparacion/', views.consultar_reparacion, name='consultar_reparacion'),
    path('consultar_cliente/', views.consultar_cliente, name='consultar_cliente'),
]