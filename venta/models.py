from django.db import models

# Create your models here.

class Client(models.Model):
    cedula = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    