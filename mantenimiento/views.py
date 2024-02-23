from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import connection

# Create your views here.

@admin_required
@employee_denied
def importar(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'mantenimiento/importar.html', {'username': request.user.username})


@admin_required
@employee_denied
def restaurar(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'mantenimiento/restaurar.html', {'username': request.user.username})


@admin_required
@employee_denied
def compactar(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
        messages.error(
                request, 'Base de datos compactada correctamente')

    return render(request, 'mantenimiento/compactar.html', {'username': request.user.username})