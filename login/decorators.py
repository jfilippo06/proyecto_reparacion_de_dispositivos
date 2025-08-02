# login/decorators.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import UserProfile

def admin_required(view_func):
    """
    Decorador que restringe el acceso solo a:
    - Superusuarios (SUPER_USER)
    - Administradores (ADMIN)
    Redirige a login si no está autenticado o muestra error 403 si no tiene permisos
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type not in [UserProfile.SUPER_USER, UserProfile.ADMIN]:
            messages.error(request, 'Acceso restringido: Se requieren privilegios de administrador')
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_denied(view_func):
    """
    Decorador que bloquea específicamente a empleados (EMPLOYEE)
    Permite a clientes (CLIENT), admins (ADMIN) y superusuarios (SUPER_USER)
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == UserProfile.EMPLOYEE:
            messages.warning(request, 'Los empleados no tienen acceso a esta sección')
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def otp_verified_required(view_func):
    """
    Decorador que verifica si el usuario completó la verificación en dos pasos
    Redirige a la página de verificación OTP si no está verificado
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_verified:
            messages.error(
                request,
                'Verificación requerida: Por favor completa el proceso de autenticación en dos pasos'
            )
            return HttpResponseRedirect(reverse('verify_otp'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(*allowed_roles):
    """
    Decorador genérico para validar múltiples roles
    Uso: @role_required(UserProfile.ADMIN, UserProfile.SUPER_USER)
    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type not in allowed_roles:
                messages.error(
                    request,
                    f'Acceso restringido: Se requieren los roles {", ".join(allowed_roles)}'
                )
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator