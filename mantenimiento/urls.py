from django.urls import path
from . import views

urlpatterns = [
    path('importar/', views.importar, name='importar'),
    path('restaurar/', views.restaurar, name='restaurar'),
    path('compactar/', views.compactar, name='compactar'),
]