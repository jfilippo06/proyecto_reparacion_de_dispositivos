from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import connection
import os
import shutil
from django.conf import settings
from mantenimiento.models import Copia_de_seguridad

# Create your views here.


@admin_required
@employee_denied
def importar(request):

    if request.method == 'GET':
        pass
    
    elif request.method == 'POST':
        # Crea la ruta al directorio
        dir_path = os.path.join(
            settings.BASE_DIR, 'mantenimiento', 'static', 'copia_de_seguridad',)

        # Asegúrate de que el directorio exista
        os.makedirs(dir_path, exist_ok=True)

        # Ruta de la base de datos actual
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

        # Obtiene una lista de todos los archivos en el directorio
        files = os.listdir(dir_path)

        # Encuentra el número más alto en los nombres de los archivos existentes
        highest_num = 0
        for file in files:
            if file.startswith('db') and file.endswith('.sqlite3'):
                num = int(file.replace('db', '').replace('.sqlite3', ''))
                highest_num = max(highest_num, num)

        # Incrementa el número más alto para el nuevo archivo
        new_num = highest_num + 1

        # Ruta de la nueva copia de la base de datos
        new_db_path = os.path.join(dir_path, f'db{new_num}.sqlite3')
        
        copia = Copia_de_seguridad.objects.create(
            copia=f'db{new_num}.sqlite3',  link=new_db_path)
        copia.save()

        # Copia la base de datos al nuevo directorio
        shutil.copy2(db_path, new_db_path)
        messages.success(
            request, 'Copia de seguridad creada correctamente.')

        
    direccion = Copia_de_seguridad.objects.all()
    paginator = Paginator(direccion, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'mantenimiento/importar.html', {'username': request.user.username, 'direccion': page_obj})



@admin_required
@employee_denied
def restaurar(request):
    if request.method == 'GET':
        direccion = Copia_de_seguridad.objects.all()
        paginator = Paginator(direccion, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        pass

    return render(request, 'mantenimiento/restaurar.html', {'username': request.user.username, 'direccion': page_obj})


def copiar_bd(request, id):
    db = Copia_de_seguridad.objects.get(id=id)

    # Ruta de la base de datos actual
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    # Copia la base de datos al nuevo directorio
    shutil.copy2(db.link, db_path)
    messages.success(
            request, 'xopia de seguridad restaurada correctamente.')

    return redirect('restaurar')


@admin_required
@employee_denied
def compactar(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
        messages.success(
            request, 'Base de datos compactada correctamente.')

    return render(request, 'mantenimiento/compactar.html', {'username': request.user.username})
