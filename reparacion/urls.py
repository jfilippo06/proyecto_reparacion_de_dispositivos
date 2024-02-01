from django.urls import path
from . import views

urlpatterns = [
    path('', views.reparacion, name='reparacion'),
    path('registrar/', views.registrarReparacion, name='registrar'),
    path('cancelar/', views.cancelar, name='cancelar'),
    path('deshabilitar/<int:id>', views.deleteReparacion, name='deshabilitar'),
    path('actualizar/<int:id>', views.updateReparacion, name='actualizar'),
]