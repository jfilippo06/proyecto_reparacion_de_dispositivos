from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    CLIENT = 'client'
    SUPER_USER = 'super_user'
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee'),
        (CLIENT, 'Client'),
        (SUPER_USER, 'Super_user'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CLIENT,
    )

    REQUIRED_FIELDS = ['user_type']