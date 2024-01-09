from django.db import models
from inventario.models import Inventario

# Create your models here.

class Client(models.Model):
    cedula = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

class N_Recibo(models.Model):
    n_recibo = models.IntegerField()

class T_Lista(models.Model):
    articulo = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    costo_unidad = models.IntegerField()
    total = models.IntegerField()
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    