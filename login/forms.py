# login/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from .models import UserProfile
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=65)
    email = forms.EmailField()
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        
        # Validar dominio de email
        domain = email.split('@')[-1]
        if domain not in settings.ALLOWED_EMAIL_DOMAINS:
            raise ValidationError("Solo se permiten correos de Gmail, Hotmail o Outlook.")
            
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
            
        return cleaned_data

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu código OTP'}))
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("El código OTP debe ser un número de 6 dígitos.")
        
        if self.user and not self.user.verify_otp(otp):
            raise ValidationError("Código OTP inválido o expirado.")
            
        return otp