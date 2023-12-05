from login.decorators import admin_required
from django.shortcuts import render


@admin_required
def computadora(request):
    if request.method == 'GET':
        return render(request, 'inventario/computadora.html', {'username': request.user.username, 'user_type':request.user.user_type})


@admin_required
def telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/telefono.html', {'username': request.user.username, 'user_type':request.user.user_type})


@admin_required
def repuesto_computadora(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_computadora.html', {'username': request.user.username, 'user_type':request.user.user_type})


@admin_required
def repuesto_telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_telefono.html', {'username': request.user.username, 'user_type':request.user.user_type})


@admin_required
def acessorio(request):
    if request.method == 'GET':
        return render(request, 'inventario/accesorio.html', {'username': request.user.username, 'user_type':request.user.user_type})
