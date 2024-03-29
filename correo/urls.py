from django.urls import path
from . import views

urlpatterns = [
    path('', views.correo_enviado, name='correo_enviado'),
    path('correo_no_enviado/', views.correo, name='correo_no_enviado'),
    path('enviar_correo/<int:id>', views.enviar_correo, name='enviar_correo'),
    path('crear_correo/', views.crear_correo, name='crear_correo'),
    path('enviar_todo/', views.enviar_todo, name='enviar_todo'),
]