from django.shortcuts import render, redirect, get_object_or_404
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from reparacion.models import Reparacion
from django.contrib import messages
from venta.models import Client
# Create your views here.


@admin_required
@employee_denied
def reparacion(request):
    if request.method == 'GET':
        reparacion = Reparacion.objects.all().exclude(is_active=False)
        paginator = Paginator(reparacion, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        reparacion = request.POST['table_search']
        user_type = request.POST['user_type']
        if reparacion == '':
            return redirect('reparacion')
        else:
            computadora = Reparacion.objects.filter(
                **{user_type+'__iexact': reparacion}).exclude(is_active=False)
        paginator = Paginator(computadora, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'reparacion/reparacion.html', {'username': request.user.username, 'reparaciones': page_obj})


@admin_required
@employee_denied
def registrarReparacion(request):
    if request.method == 'GET':
        return render(request, 'reparacion/registrar.html', {'username': request.user.username})

    elif request.method == 'POST':
        articulo = request.POST['articulo'].lower().capitalize()
        descripcion = request.POST['descripcion'].lower().capitalize()
        cantidad = request.POST['cantidad']
        cedula = request.POST['cedula']
        nombre = request.POST['nombre'].lower().capitalize()
        correo = request.POST['correo'].lower().capitalize()
        estado = request.POST['estado']

        try:
            usuario = Client.objects.get(cedula=cedula)
            save = Reparacion.objects.create(articulo=articulo, descripcion=descripcion, cantidad=cantidad,
                                             cedula=cedula, username=nombre, email=correo, estado=estado, is_active=True, client_id=usuario.id)
            save.save()
        except Client.DoesNotExist:
            cliente = Client.objects.create(
                cedula=cedula, username=nombre, email=correo)
            cliente.save()
            usuario = Client.objects.get(cedula=cedula)
            save = Reparacion.objects.create(articulo=articulo, descripcion=descripcion, cantidad=cantidad,
                                             cedula=cedula, username=nombre, email=correo, estado=estado, is_active=True, client_id=usuario.id)
            save.save()

        return redirect('reparacion')


def cancelar(request):
    return redirect('reparacion')


@admin_required
@employee_denied
def deleteReparacion(request, id):
    reparacion = get_object_or_404(Reparacion, id=id)
    reparacion.is_active = False
    reparacion.save()
    return redirect('reparacion')


def updateReparacion(request, id):
    if request.method == "GET":
        reparacion = get_object_or_404(Reparacion, id=id)
        if reparacion.is_active == False:
            return redirect('reparacion')
        return render(request, 'reparacion/editar_reparacion.html', {
            'username': request.user.username,
            'reparacion_id': id,
            'articulo': reparacion.articulo,
            'descripcion': reparacion.descripcion,
            'cantidad': reparacion.cantidad,
            'estado': reparacion.estado,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Reparacion.objects.get(pk=id)

            # Actualiza los campos del objeto con los nuevos valores
            objeto.articulo = request.POST['articulo'].lower().capitalize()
            objeto.descripcion = request.POST['descripcion'].lower(
            ).capitalize()
            objeto.cantidad = request.POST['cantidad']
            objeto.estado = request.POST['estado']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('reparacion')
        except Reparacion.DoesNotExist:
            messages.error(
                request, '...')
            return redirect('reparacion')


def buscar_cedula(request):
    try:
        table_search = request.POST['table_search']
        usuario = Client.objects.get(cedula=table_search)
        return render(request, 'reparacion/registrar.html', {'username': request.user.username, 'cedula': usuario.cedula, 'nombre': usuario.username})
    except Client.DoesNotExist:
        messages.error(
            request, 'Usuario no existe')
        return redirect('registrar')
