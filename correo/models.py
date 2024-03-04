from django.db import models
from venta.models import N_Recibo, Client
# Create your models here.

class Correo_enviado(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    cedula = models.IntegerField()
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    link = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Correo_no_enviado(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    cedula = models.IntegerField()
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    link = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
