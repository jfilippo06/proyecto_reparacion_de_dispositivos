from django.urls import path
from . import views

urlpatterns = [
    path('', views.correo, name='correo')
]