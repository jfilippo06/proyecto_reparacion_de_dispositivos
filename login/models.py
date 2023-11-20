from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    CLIENT = 'client'
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee'),
        (CLIENT, 'Client'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CLIENT,
    )

    REQUIRED_FIELDS = ['user_type']