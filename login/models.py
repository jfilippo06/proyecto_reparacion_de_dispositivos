# login/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import pyotp
from datetime import timedelta
from requests
from django.conf import settings

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
    is_verified = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    
    REQUIRED_FIELDS = ['user_type']
    
    def generate_otp(self):
        """Genera un nuevo OTP secreto y lo guarda"""
        self.otp_secret = pyotp.random_base32()
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_secret
    
    def get_otp(self):
        """Genera el código OTP actual basado en el secreto"""
        if not self.otp_secret:
            return None
        totp = pyotp.TOTP(self.otp_secret, interval=settings.OTP_EXPIRE_SECONDS)
        return totp.now()
    
    def verify_otp(self, otp):
        """Verifica si el OTP proporcionado es válido"""
        if not self.otp_secret or not self.otp_created_at:
            return False
            
        # Verificar si el OTP ha expirado
        expiry_time = self.otp_created_at + timedelta(seconds=settings.OTP_EXPIRE_SECONDS)
        if timezone.now() > expiry_time:
            return False
            
        totp = pyotp.TOTP(self.otp_secret, interval=settings.OTP_EXPIRE_SECONDS)
        return totp.verify(otp)