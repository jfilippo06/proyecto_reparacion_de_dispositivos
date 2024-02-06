from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from venta.models import Direccion_de_factura
from django.core.paginator import Paginator
from reparacion.models import Reparacion

# Create your views here.


@admin_required
@employee_denied
def recibo(request):
    if request.method == 'GET':
        direccion = Direccion_de_factura.objects.all()
        paginator = Paginator(direccion, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'reporte/recibo.html', {'username': request.user.username, 'user_type': request.user, 'reporte': page_obj})

    elif request.method == 'POST':
        reporte = request.POST['table_search']
        user_type = request.POST['user_type']
        if reporte == '':
            return redirect('recibo')
        else:
            computadora = Direccion_de_factura.objects.filter(
                **{user_type+'__iexact': reporte})
        paginator = Paginator(computadora, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'reporte/recibo.html', {'username': request.user.username, 'user_type': request.user, 'reporte': page_obj})


@admin_required
@employee_denied
def reporteRepaciones(request):
    if request.method == 'GET':
        reparacion = Reparacion.objects.all()
        paginator = Paginator(reparacion, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        pass

    return render(request, 'reporte/reparacion.html', {'username': request.user.username, 'reparaciones': page_obj})


@admin_required
@employee_denied
def reporteCliente(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'reporte/cliente.html', {'username': request.user.username})


@admin_required
@employee_denied
def reporteInventario(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'reporte/inventario.html', {'username': request.user.username})


@admin_required
@employee_denied
def reporteVenta(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'reporte/venta.html', {'username': request.user.username})
