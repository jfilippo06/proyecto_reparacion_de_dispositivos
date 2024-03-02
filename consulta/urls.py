from django.urls import path
from . import views

urlpatterns = [
    path('consultar_inventario/', views.consultar_inventario, name='consultar_inventario'),
]