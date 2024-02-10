from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from venta.models import Direccion_de_factura
from django.core.paginator import Paginator
from reparacion.models import Reparacion
from venta.models import Totales
from venta.views import impuesto
from django.db.models import Q
from datetime import datetime, time


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
        elif user_type == 'n_recibo_id':
            computadora = Direccion_de_factura.objects.filter(
                **{user_type: reporte})
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
        date_begin = datetime.strptime(request.POST.get('date_begin', ''), '%Y-%m-%d') if request.POST.get(
            'date_begin', '') else datetime.combine(datetime.today(), time.min)
        date_end = datetime.strptime(request.POST.get(
            'date_end', ''), '%Y-%m-%d') if request.POST.get('date_end', '') else datetime.now()
        table_search = request.POST['table_search']

        query = Q()

        if request.POST['user_type'] in ['ER', 'EC', 'TR']:
            query &= Q(estado=request.POST['user_type'])
        elif request.POST['user_type'] == 'cliente':
            if table_search:
                query &= Q(username=table_search)
        elif request.POST['user_type'] == 'cedula':
            if table_search:
                query &= Q(cedula=table_search)
        elif request.POST['user_type'] == 'todos':
            pass

        query &= Q(fecha_creacion__range=(date_begin, date_end))

        reparaciones = Reparacion.objects.filter(query)

        if 'buscar' in request.POST['submit_button']:
            paginator = Paginator(reparaciones, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
        elif 'enviar' in request.POST['submit_button']:
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
        venta = Totales.objects.all()
        paginator = Paginator(venta, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        iva = impuesto()

    elif request.method == 'POST':
        pass

    return render(request, 'reporte/venta.html', {'username': request.user.username, 'ventas': page_obj, 'is_active': iva})
