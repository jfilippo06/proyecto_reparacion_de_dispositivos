from django.urls import path
from . import views

urlpatterns = [
    path('', views.correo, name='correo'),
    path('enviar_correo/<int:id>', views.enviar_correo, name='enviar_correo')
]