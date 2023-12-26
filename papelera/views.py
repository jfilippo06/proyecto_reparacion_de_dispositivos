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
    return redirect('papelera_usuario')


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


@admin_required
@employee_denied
def habilitar_computadoras(request, id):
    user = get_object_or_404(Inventario, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_computadora')

@admin_required
@employee_denied
def telefono(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='TEL').exclude(is_active=True)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/telefono.html', {'username': request.user.username, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('papelera_telefono')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='TEL', codigo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='TEL', articulo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='TEL', marca__iexact=inventario).exclude(is_active=True)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='TEL', modelo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='TEL', no_serie__iexact=inventario).exclude(is_active=True)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='TEL', cantidad=inventario).exclude(is_active=True)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='TEL', costo=inventario).exclude(is_active=True)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
@employee_denied
def habilitar_telefonos(request, id):
    user = get_object_or_404(Inventario, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_telefono')

@admin_required
@employee_denied
def repuesto_computadora(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='RPC').exclude(is_active=True)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/repuesto_computadora.html', {'username': request.user.username, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('papelera_repuesto_computadora')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='RPC', codigo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='RPC', articulo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='RPC', marca__iexact=inventario).exclude(is_active=True)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='RPC', modelo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='RPC', no_serie__iexact=inventario).exclude(is_active=True)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='RPC', cantidad=inventario).exclude(is_active=True)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='RPC', costo=inventario).exclude(is_active=True)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/repuesto_computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

@admin_required
@employee_denied
def habilitar_repuesto_computadora(request, id):
    user = get_object_or_404(Inventario, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_repuesto_computadora')

@admin_required
@employee_denied
def repuesto_telefono(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='RPT').exclude(is_active=True)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/repuesto_telefono.html', {'username': request.user.username, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('papelera_repuesto_telefono')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='RPT', codigo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='RPT', articulo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='RPT', marca__iexact=inventario).exclude(is_active=True)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='RPT', modelo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='RPT', no_serie__iexact=inventario).exclude(is_active=True)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='RPT', cantidad=inventario).exclude(is_active=True)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='RPT', costo=inventario).exclude(is_active=True)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/repuesto_telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

@admin_required
@employee_denied
def habilitar_repuesto_telefono(request, id):
    user = get_object_or_404(Inventario, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_repuesto_telefono')

@admin_required
@employee_denied
def accesorio(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='ASE').exclude(is_active=True)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/accesorio.html', {'username': request.user.username, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('papelera_accesorio')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='ASE', codigo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='ASE', articulo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='ASE', marca__iexact=inventario).exclude(is_active=True)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='ASE', modelo__iexact=inventario).exclude(is_active=True)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='ASE', no_serie__iexact=inventario).exclude(is_active=True)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='ASE', cantidad=inventario).exclude(is_active=True)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='ASE', costo=inventario).exclude(is_active=True)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/accesorio.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

@admin_required
@employee_denied
def habilitar_accesorio(request, id):
    user = get_object_or_404(Inventario, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_accesorio')