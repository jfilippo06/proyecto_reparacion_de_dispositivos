from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def computadora(request):
    if request.method == 'GET':
        return render(request, 'inventario/computadora.html', {'user_name': request.user.username})


@login_required
def telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/telefono.html', {'user_name': request.user.username})


@login_required
def repuesto_computadora(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_computadora.html', {'user_name': request.user.username})


@login_required
def repuesto_telefono(request):
    if request.method == 'GET':
        return render(request, 'inventario/repuesto_telefono.html', {'user_name': request.user.username})


@login_required
def acessorio(request):
    if request.method == 'GET':
        return render(request, 'inventario/accesorio.html', {'user_name': request.user.username})
