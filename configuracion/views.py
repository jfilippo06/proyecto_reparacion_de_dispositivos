from login.decorators import admin_required, employee_denied
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from login.models import UserProfile
from django.core.paginator import Paginator
from configuracion.models import Impuesto, Dolar

# Create your views here.


@admin_required
@employee_denied
def users(request):
    if request.method == 'GET':
        usuarios = UserProfile.objects.exclude(
            user_type='super_user').exclude(is_active=False)
        paginator = Paginator(usuarios, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'configuracion/usuarios.html', {'username': request.user.username, 'usuarios': page_obj})

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
        if user.user_type == "super_user" or user.is_active == False:
            return redirect('usuarios')
        return render(request, 'configuracion/editar_usuarios.html', {
            'email': user.email,
            'username': request.user.username,
            'username_edit': user.username,
            'user_type': user.user_type,
            'usuario': id
        })

    elif request.method == "POST":
        User = get_user_model()

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            messages.error(request, 'Usuario no existe')
            return redirect('usuarios')

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = request.POST['user_type']  # Set user_type as 'client'

        # Check if a user with this username or email already exists
        if User.objects.filter(username=username).exclude(pk=id).exists():
            messages.error(request, 'Usuario ya existe')
            return redirect('usuarios')
        elif User.objects.filter(email=email).exclude(pk=id).exists():
            messages.error(
                request, 'Correo electronico esta siendo utilizado por otro usuarios')
            return redirect('usuarios')

        # Update the user
        user.username = username
        user.set_password(password)  # Use set_password to hash the password
        user.email = email
        user.user_type = user_type
        user.save()

        messages.success(request, 'Usuario actualizado correctamente')
        return redirect('usuarios')


@admin_required
@employee_denied
def deleteUsers(request, id):
    user = get_object_or_404(UserProfile, id=id)
    user.is_active = False
    user.save()
    return redirect('usuarios')


@admin_required
@employee_denied
def cancelar(request):
    return redirect('usuarios')


@admin_required
@employee_denied
def buscar(request):
    username = request.POST['table_search']
    if username == '':
        return redirect('usuarios')
    user = UserProfile.objects.filter(username=username).exclude(
        user_type='super_user').exclude(is_active=False)
    return render(request, 'configuracion/usuarios.html', {'username': request.user.username, 'usuarios': user})


@admin_required
@employee_denied
def impuesto(request):
    if request.method == 'GET':
        impuesto = Impuesto.objects.all()
        return render(request, 'impuesto/impuesto.html', {'username': request.user.username, 'impuestos': impuesto})


@admin_required
@employee_denied
def activar_impuesto(request):
    iva = Impuesto.objects.get(id=1)
    iva.is_active = True
    iva.save()
    return redirect('impuesto')


@admin_required
@employee_denied
def desactivar_impuesto(request):
    iva = Impuesto.objects.get(id=1)
    iva.is_active = False
    iva.save()
    return redirect('impuesto')


@admin_required
@employee_denied
def actualizar_impuesto(request):
    iva = request.POST['iva']
    valor = float(request.POST['valor'])
    impuesto = Impuesto.objects.get(id=1)
    impuesto.iva = iva
    impuesto.valor = valor
    impuesto.save()
    return redirect('impuesto')


@admin_required
@employee_denied
def dolar(request):
    if request.method == 'GET':
        dolar = Dolar.objects.all()
        return render(request, 'dolar/dolar.html', {'username': request.user.username, 'dolar': dolar})


@admin_required
@employee_denied
def activar_dolar(request):
    dolar = Dolar.objects.get(id=1)
    dolar.is_active = True
    dolar.save()
    return redirect('dolar')


@admin_required
@employee_denied
def desactivar_dolar(request):
    dolar = Dolar.objects.get(id=1)
    dolar.is_active = False
    dolar.save()
    return redirect('dolar')


@admin_required
@employee_denied
def actualizar_dolar(request):
    moneda = request.POST['moneda']
    valor = float(request.POST['valor'])
    dolar = Dolar.objects.get(id=1)
    dolar.moneda = moneda
    dolar.valor = valor
    dolar.save()
    return redirect('dolar')
