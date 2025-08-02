# login/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RegisterForm, OTPVerificationForm
from .models import UserProfile
from .decorators import admin_required, employee_denied
from django.utils import timezone
from datetime import timedelta

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('computadora')  # Cambia esto por tu vista principal
            
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})
        
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                if not user.is_verified:
                    # Si el usuario no está verificado, enviar OTP nuevamente
                    user.generate_otp()
                    send_otp_email(user)
                    request.session['otp_user_id'] = user.id
                    return redirect('verify_otp')
                    
                login(request, user)
                messages.success(request, f'Bienvenido {user.username}.')
                
                # Redirección según tipo de usuario
                if user.user_type in [UserProfile.SUPER_USER, UserProfile.ADMIN, UserProfile.EMPLOYEE]:
                    return redirect('computadora')
                elif user.user_type == UserProfile.CLIENT:
                    return redirect('usuarios')
                    
        # Si el formulario no es válido o la autenticación falla
        messages.error(request, 'Usuario o contraseña no válido.')
        return render(request, 'login/login.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('computadora')
            
        return render(request, 'register/register.html', {'form': RegisterForm()})
        
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            
            # Verificar si el usuario ya existe
            if UserProfile.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
                return render(request, 'register/register.html', {'form': form})
                
            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
                return render(request, 'register/register.html', {'form': form})
                
            # Crear usuario
            user = UserProfile.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type
            )
            
            # Generar y enviar OTP
            user.generate_otp()
            send_otp_email(user)
            
            # Guardar user.id en sesión para verificación
            request.session['otp_user_id'] = user.id
            messages.success(request, 'Registro exitoso. Por favor verifica tu email con el código OTP.')
            return redirect('verify_otp')
            
        return render(request, 'register/register.html', {'form': form})

def verify_otp(request):
    if not request.session.get('otp_user_id'):
        messages.error(request, 'Sesión no válida para verificación OTP.')
        return redirect('login')
        
    try:
        user = UserProfile.objects.get(id=request.session['otp_user_id'])
    except UserProfile.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('login')
        
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user=user)
        
        if form.is_valid():
            # Verificación exitosa
            user.is_verified = True
            user.save()
            
            # Limpiar sesión
            if 'otp_user_id' in request.session:
                del request.session['otp_user_id']
                
            # Autenticar al usuario
            login(request, user)
            messages.success(request, 'Verificación exitosa. ¡Bienvenido!')
            
            # Redirección según tipo de usuario
            if user.user_type in [UserProfile.SUPER_USER, UserProfile.ADMIN, UserProfile.EMPLOYEE]:
                return redirect('computadora')
            elif user.user_type == UserProfile.CLIENT:
                return redirect('usuarios')
                
    else:
        form = OTPVerificationForm(user=user)
        
    return render(request, 'login/verify_otp.html', {'form': form})

def resend_otp(request):
    if not request.session.get('otp_user_id'):
        messages.error(request, 'Sesión no válida.')
        return redirect('login')
        
    try:
        user = UserProfile.objects.get(id=request.session['otp_user_id'])
    except UserProfile.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('login')
        
    # Generar nuevo OTP
    user.generate_otp()
    send_otp_email(user)
    
    messages.success(request, 'Se ha enviado un nuevo código OTP a tu correo.')
    return redirect('verify_otp')

def send_otp_email(user):
    """Envía el código OTP al email del usuario"""
    otp_code = user.get_otp()
    subject = 'Tu código de verificación'
    message = f'''
    Hola {user.username},
    
    Tu código de verificación es: {otp_code}
    
    Este código expirará en {settings.OTP_EXPIRE_SECONDS // 60} minutos.
    
    Si no solicitaste este código, por favor ignora este mensaje.
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@admin_required
def admin_dashboard(request):
    # Vista solo para administradores
    return render(request, 'admin/dashboard.html')

@employee_denied
def client_dashboard(request):
    # Vista para clientes (no empleados)
    return render(request, 'client/dashboard.html')