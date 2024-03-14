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
    total = models.BigIntegerField()
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class Factura(models.Model):
    articulo = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    costo_unidad = models.IntegerField()
    total = models.IntegerField()
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class Totales(models.Model):
    sub_total = models.IntegerField()
    iva = models.DecimalField(max_digits=100, decimal_places=2)
    total = models.DecimalField(max_digits=100, decimal_places=2)
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class Direccion_de_factura(models.Model):
    link = models.CharField(max_length=300)
    nombre_cliente = models.CharField(max_length=100)
    cedula = models.IntegerField()
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class Cliente_atendido(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    cedula = models.IntegerField()
    n_recibo = models.ForeignKey(N_Recibo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    sub_total = models.IntegerField()
    iva = models.DecimalField(max_digits=100, decimal_places=2)
    total = models.DecimalField(max_digits=100, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


