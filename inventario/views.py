from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inventario_computadora(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'inventario/inventario_computadora.html', {'user_name':request.user.username})

@login_required
def inventario_telefono(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'inventario/inventario_telefono.html', {'user_name':request.user.username})

@login_required
def inventario_repuesto_computadora(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'inventario/inventario_repuesto_computadora.html', {'user_name':request.user.username})

@login_required
def inventario_repuesto_telefono(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'inventario/inventario_repuesto_telefono.html', {'user_name':request.user.username})

@login_required
def inventario_acessorio(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'inventario/inventario_accesorio.html', {'user_name':request.user.username})