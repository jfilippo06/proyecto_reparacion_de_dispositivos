from login.decorators import admin_required
from django.shortcuts import render, redirect, get_object_or_404
from inventario.models import Inventario
from django.core.paginator import Paginator


@admin_required
def computadora(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='COM').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('computadora')
        elif user_type == 'codigo':
            computadora = Inventario.objects.filter(
                categoria='COM', codigo=inventario).exclude(is_active=False)
        elif user_type == 'articulo':
            computadora = Inventario.objects.filter(
                categoria='COM', articulo=inventario).exclude(is_active=False)
        elif user_type == 'marca':
            computadora = Inventario.objects.filter(
                categoria='COM', marca=inventario).exclude(is_active=False)
        elif user_type == 'modelo':
            computadora = Inventario.objects.filter(
                categoria='COM', modelo=inventario).exclude(is_active=False)
        elif user_type == 'no_serie':
            computadora = Inventario.objects.filter(
                categoria='COM', no_serie=inventario).exclude(is_active=False)
        elif user_type == 'cantidad':
            computadora = Inventario.objects.filter(
                categoria='COM', cantidad=inventario).exclude(is_active=False)
        elif user_type == 'costo':
            computadora = Inventario.objects.filter(
                categoria='COM', costo=inventario).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteComputadora(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('computadora')


@admin_required
def telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/telefono.html', {'username': request.user.username, 'user_type': request.user.user_type})


@admin_required
def repuesto_computadora(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_computadora.html', {'username': request.user.username, 'user_type': request.user.user_type})


@admin_required
def repuesto_telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_telefono.html', {'username': request.user.username, 'user_type': request.user.user_type})


@admin_required
def acessorio(request):
    if request.method == 'GET':
        return render(request, 'inventario/accesorio.html', {'username': request.user.username, 'user_type': request.user.user_type})
