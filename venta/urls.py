from django.urls import path
from . import views

urlpatterns = [
    path('consultar_cliente/', views.client, name='cliente'),
]