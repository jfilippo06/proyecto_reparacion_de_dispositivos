from django.urls import path
from . import views

urlpatterns = [
    path('recibo/', views.recibo, name='recibo'),
]