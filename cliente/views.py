from django.shortcuts import render, redirect
from login.decorators import admin_required
from django.contrib import messages
from venta.models import Client

# Create your views here.

@admin_required
def registrar_cliente(request):
    if request.method == 'GET':
        return render(request, 'cliente/registrar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type})

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

        messages.success(request, 'Cliente registrado correctamente.')
        return redirect('registrar_cliente')