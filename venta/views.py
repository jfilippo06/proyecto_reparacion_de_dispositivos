from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from venta.models import Client

# Create your views here.


@admin_required
@employee_denied
def client(request):
    if request.method == 'GET':
        return render(request, 'venta/consultar_cliente.html', {'username': request.user.username})

    elif request.method == 'POST':
        cedula = request.POST['cedula']
        if Client.objects.filter(cedula=cedula):
            return redirect('facturar_cliente')
        else:
            return redirect('registrar_cliente')



@admin_required
@employee_denied
def registrar_cliente(request):
    if request.method == 'GET':
        return render(request, 'venta/registrar_cliente.html', {'username': request.user.username})

    elif request.method == 'POST':
        pass


@admin_required
@employee_denied
def facturar_cliente(request):
    if request.method == 'GET':
        return render(request, 'venta/facturar_cliente.html', {'username': request.user.username})

    elif request.method == 'POST':
        pass
