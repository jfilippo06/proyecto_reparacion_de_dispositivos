# login/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import UserProfile
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass123',
            user_type='client'
        )
        self.admin = UserProfile.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='adminpass123',
            user_type='admin'
        )

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de login

    def test_failed_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña no válido.')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'user_type': 'client'
        })
        self.assertEqual(response.status_code, 302)  # Redirección a verificación OTP
        self.assertEqual(len(mail.outbox), 1)  # Verificar que se envió el email

    def test_otp_verification(self):
        # Primero registramos un usuario
        self.client.post(reverse('register'), {
            'username': 'otpuser',
            'email': 'otpuser@gmail.com',
            'password': 'otppass123',
            'confirm_password': 'otppass123',
            'user_type': 'client'
        })
        
        # Obtenemos el usuario creado
        user = UserProfile.objects.get(username='otpuser')
        otp = user.get_otp()
        
        # Verificamos el OTP
        session = self.client.session
        session['otp_user_id'] = user.id
        session.save()
        
        response = self.client.post(reverse('verify_otp'), {
            'otp': otp
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de verificación
        
        # Verificamos que el usuario está marcado como verificado
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

    def test_expired_otp(self):
        user = UserProfile.objects.create_user(
            username='expireduser',
            email='expired@gmail.com',
            password='expiredpass123',
            user_type='client'
        )
        user.generate_otp()
        user.otp_created_at = timezone.now() - timedelta(seconds=settings.OTP_EXPIRE_SECONDS + 60)
        user.save()
        
        session = self.client.session
        session['otp_user_id'] = user.id
        session.save()
        
        response = self.client.post(reverse('verify_otp'), {
            'otp': user.get_otp()
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Código OTP inválido o expirado')

    def test_admin_access(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_employee_denied_access(self):
        employee = UserProfile.objects.create_user(
            username='employee',
            email='employee@gmail.com',
            password='employeepass123',
            user_type='employee'
        )
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get(reverse('client_dashboard'))
        self.assertEqual(response.status_code, 403)  # Acceso prohibido