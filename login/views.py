from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm

# Create your views here.


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('computadora')

        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.user_type == 'super_user' or user.user_type == 'admin' or user.user_type == 'employee':
                login(request, user)
                messages.error(request, f'Bienvenido {user.username}.')
                return redirect('computadora')
            elif user.user_type == 'client':
                login(request, user)
                return redirect('usuarios')

        # form is not valid or user is not authenticated
        messages.error(request, 'Usuario o contraseña no valido.')
        return render(request, 'login/login.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('computadora')

        return render(request, 'register/register.html')

    elif request.method == 'POST':
        User = get_user_model()
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = 'client'  # Set user_type as 'client'

        # Check if a user with this username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return render(request, 'register/register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return render(request, 'register/register.html')

        # Create the user
        user = User.objects.create_user(
            username=username, password=password, email=email, user_type=user_type)
        user.save()

        messages.success(request, 'User registered successfully')
        return redirect('login')
