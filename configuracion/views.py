from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


@login_required
def users(request):
    if request.method == 'GET':
        return render(request, 'configuracion/usuarios.html', {'user_name': request.user.username})

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
