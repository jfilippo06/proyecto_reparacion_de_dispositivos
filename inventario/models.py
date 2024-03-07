from django.db import models

# Create your models here.

class Inventario(models.Model):
    CATEGORIAS = [
        ('COM', 'Computadora'),
        ('TEL', 'Telefono'),
        ('ASE', 'Asesorios'),
        ('RPC', 'Repuestos de Computadoras'),
        ('RPT', 'Repuestos de Telefonos'),
    ]

    codigo = models.CharField(unique=True, max_length=6)
    articulo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    no_serie = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True)
    cantidad = models.PositiveIntegerField()
    costo = models.IntegerField()
    categoria = models.CharField(max_length=3, choices=CATEGORIAS)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()