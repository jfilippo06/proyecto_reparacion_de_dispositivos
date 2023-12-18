from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from login.models import UserProfile
from inventario.models import Inventario
from django.core.paginator import Paginator

# Create your views here.


@admin_required
@employee_denied
def usuarios(request):
    if request.method == 'GET':
        usuarios = UserProfile.objects.filter(
            is_active=False).exclude(user_type='super_user')
        paginator = Paginator(usuarios, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/usuarios.html', {'username': request.user.username, 'usuarios': page_obj})

    elif request.method == 'POST':
        username = request.POST['table_search']
        if username == '':
            return redirect('papelera_usuarios')
        user = UserProfile.objects.filter(username=username).exclude(
            user_type='super_user').exclude(is_active=True)
        return render(request, 'papelera/usuarios.html', {'username': request.user.username, 'usuarios': user})


@admin_required
@employee_denied
def habilitar_usuarios(request, id):
    user = get_object_or_404(UserProfile, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_usuarios')


@admin_required
@employee_denied
def computadora(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='COM').exclude(is_active=True)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/computadora.html', {'username': request.user.username, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('papelera_computadora')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='COM', codigo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='COM', articulo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='COM', marca__iexact=inventario).exclude(is_active=True)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='COM', modelo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='COM', no_serie__iexact=inventario).exclude(is_active=True)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='COM', cantidad=inventario).exclude(is_active=True)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='COM', costo=inventario).exclude(is_active=True)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})
