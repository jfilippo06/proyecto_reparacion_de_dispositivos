from django.db import models
from venta.models import Client

# Create your models here.

class Reparacion(models.Model):
    CATEGORIAS = [
        ('ER', 'En_Revision'),
        ('EC', 'En_Curso'),
        ('TR', 'Terminado'),
    ]

    articulo = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=35)
    cantidad = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cedula = models.IntegerField()
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    estado = models.CharField(max_length=3, choices=CATEGORIAS)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
