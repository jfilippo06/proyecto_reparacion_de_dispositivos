from django.db import models

# Create your models here.

class Copia_de_seguridad(models.Model):
    copia = models.CharField(max_length=100)
    link = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)