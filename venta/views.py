from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from venta.models import Client
from inventario.models import Inventario

# Create your views here.


@admin_required
@employee_denied
def client(request):
    if request.method == 'GET':
        return render(request, 'venta/consultar_cliente.html', {'username': request.user.username})

    elif request.method == 'POST':
        cedula = request.POST['cedula']
        request.session['cedula'] = cedula
        if Client.objects.filter(cedula=cedula):
            return redirect('facturar_cliente')
        else:
            return redirect('registrar_cliente')


@admin_required
@employee_denied
def registrar_cliente(request):
    if request.method == 'GET':
        cedula = request.session.get('cedula')
        return render(request, 'venta/registrar_cliente.html', {'username': request.user.username, 'cedula': cedula})

    elif request.method == 'POST':
        cedula = request.POST['cedula']
        nombre = request.POST['nombre']
        email = request.POST['email']

        if Client.objects.filter(cedula=cedula).exists():
            messages.error(request, 'Cédula ya exite.')
            return redirect('registrar_cliente')
        elif Client.objects.filter(email=email).exists():
            messages.error(
                request, 'Correo electronico le pertenece a otro cliente.')
            return redirect('registrar_cliente')

        nuevo_cliente = Client(cedula=cedula, username=nombre, email=email)
        nuevo_cliente.save()

        return redirect('facturar_cliente')


@admin_required
@employee_denied
def cancelar(request):
    return redirect('cliente')


@admin_required
@employee_denied
def facturar_cliente(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='COM').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'venta/facturar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        pass
