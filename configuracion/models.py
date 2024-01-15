from django.db import models

# Create your models here.

class Impuesto(models.Model):
    iva = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=5, decimal_places=2)