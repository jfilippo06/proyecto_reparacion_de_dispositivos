from django.urls import path
from . import views

urlpatterns = [
    path('', views.reparacion, name='reparacion'),
    path('registrar', views.registrarReparacion, name='registrar'),
]