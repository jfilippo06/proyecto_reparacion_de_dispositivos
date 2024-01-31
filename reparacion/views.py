from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from reparacion.models import Reparacion
# Create your views here.


@admin_required
@employee_denied
def reparacion(request):
    if request.method == 'GET':
        inventario = Reparacion.objects.all().exclude(is_active=False)
        paginator = Paginator(inventario, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        pass

    return render(request, 'reparacion/reparacion.html', {'username': request.user.username, 'reparaciones': page_obj})


@admin_required
@employee_denied
def registrarReparacion(request):
    if request.method == 'GET':
        return render(request, 'reparacion/registrar.html', {'username': request.user.username})

    elif request.method == 'POST':
        articulo = request.POST['articulo']
        descripcion = request.POST['descripcion']
        cantidad = request.POST['cantidad']
        cedula = request.POST['cedula']
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        estado = request.POST['estado']

        save = Reparacion.objects.create(articulo=articulo, descripcion=descripcion, cantidad=cantidad,
                                  cedula=cedula, username=nombre, email=correo, estado=estado, is_active=True)
        save.save()
        return redirect('reparacion')
