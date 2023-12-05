from login.decorators import admin_required, employee_denied
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from login.models import UserProfile

# Create your views here.


@admin_required
@employee_denied
def users(request):
    if request.method == 'GET':
        usuarios = UserProfile.objects.exclude(
            user_type='super_user').exclude(is_active=False)
        return render(request, 'configuracion/usuarios.html', {'username': request.user.username, 'usuarios': usuarios})

    elif request.method == 'POST':
        User = get_user_model()
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = request.POST['user_type']  # Set user_type as 'client'

        # Check if a user with this username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ya existe')
            return redirect('usuarios')
        elif User.objects.filter(email=email).exists():
            messages.error(
                request, 'Correo electronico esta siendo utilizado por otro usuarios')
            return redirect('usuarios')

        # Create the user
        user = User.objects.create_user(
            username=username, password=password, email=email, user_type=user_type)
        user.save()

        messages.success(request, 'Usuario registrado correctamente')
        return redirect('usuarios')


@admin_required
@employee_denied
def updateUsers(request, id):
    if request.method == "GET":
        user = get_object_or_404(UserProfile, id=id)
        if user.user_type == "super_user":
            return redirect('usuarios')
        return render(request, 'configuracion/editar_usuarios.html', {
            'email': user.email,
            'username': request.user.username,
            'username_edit': user.username,
            'user_type': user.user_type,
        })

    if request.method == "POST":
        pass


@admin_required
@employee_denied
def deleteUsers(request, id):
    user = get_object_or_404(UserProfile, id=id)
    user.is_active = False
    user.save()
    return redirect('usuarios')
