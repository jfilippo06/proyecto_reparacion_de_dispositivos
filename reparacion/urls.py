from django.urls import path
from . import views

urlpatterns = [
    path('', views.reparacion, name='reparacion'),
    path('registrar/', views.registrarReparacion, name='registrar'),
    path('cancelar_paraciones/', views.cancelar, name='cancelar_reparaciones'),
    path('deshabilitar/<int:id>', views.deleteReparacion, name='deshabilitar'),
    path('actualizar/<int:id>', views.updateReparacion, name='actualizar'),
]