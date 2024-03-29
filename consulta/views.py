from django.shortcuts import render, redirect
from login.decorators import admin_required
from inventario.models import Inventario
from reparacion.models import Reparacion
from venta.models import Client, Factura
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, time
from django.db.models import Sum
import json

# Create your views here.


@admin_required
def consultar_inventario(request):
    if request.method == 'GET':
        if 'inventario_pop' in request.session:
            inventario_pop = request.session['inventario_pop']
            inventario = Inventario.objects.filter(id__in=inventario_pop)
        else:
            inventario = []

    elif request.method == 'POST':
        equipo = request.POST['equipo']
        user_type = request.POST['user_type']
        table_search = request.POST['table_search']

        # Define a dictionary to map user_type to the corresponding field in the model
        user_type_field_map = {
            'codigo': 'codigo__iexact',
            'articulo': 'articulo__iexact',
            'marca': 'marca__iexact',
            'modelo': 'modelo__iexact',
            'no_serie': 'no_serie__iexact',
            'cantidad': 'cantidad',
            'costo': 'costo'
        }

        # Initialize the query parameters
        query_params = {'categoria': equipo}

        # If table_search is not empty, add the corresponding field to the query parameters
        if table_search != '':
            query_params[user_type_field_map[user_type]] = table_search

        # Query the database
        inventario = Inventario.objects.filter(
            **query_params).exclude(is_active=False)
        request.session['inventario_pop'] = list(
            inventario.values_list('id', flat=True))

    paginator = Paginator(inventario, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'consulta/inventario.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def consultar_reparacion(request):
    if request.method == 'GET':
        reparacion = Reparacion.objects.all().exclude(is_active=False).order_by('-id')
        paginator = Paginator(reparacion, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        reparacion = request.POST['table_search']
        user_type = request.POST['user_type']
        if reparacion == '':
            messages.error(request, 'Introduzca texto.')
            return redirect('consulta_reparacion')
        else:
            computadora = Reparacion.objects.filter(
                **{user_type+'__iexact': reparacion}).exclude(is_active=False)
        paginator = Paginator(computadora, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'consulta/reparacion.html', {'username': request.user.username, 'user_type': request.user.user_type, 'reparaciones': page_obj})


@admin_required
def consultar_cliente(request):
    if request.method == 'GET':
        cliente = Client.objects.all().order_by('-id')
        paginator = Paginator(cliente, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        cliente = request.POST['table_search']
        user_type = request.POST['user_type']
        if cliente == '':
            messages.error(request, 'Introduzca texto.')
            return redirect('consultar_cliente')
        else:
            lista = Client.objects.filter(
                **{user_type+'__iexact': cliente})
        paginator = Paginator(lista, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'consulta/cliente.html', {'username': request.user.username, 'user_type': request.user.user_type, 'cliente': page_obj})


@admin_required
def consultar_venta(request):
    if request.method == 'GET':
        fecha_inicio =  datetime.combine(datetime.today(), time.min)
        fecha_final = datetime.now()

    elif request.method == 'POST':
        fecha_inicio = datetime.strptime(request.POST.get('date_begin', ''), '%Y-%m-%d') if request.POST.get(
            'date_begin', '') else datetime.combine(datetime.today(), time.min)
        fecha_final = datetime.strptime(request.POST.get(
            'date_end', ''), '%Y-%m-%d') if request.POST.get('date_end', '') else datetime.now()
    
    facturas = Factura.objects.filter(fecha_creacion__range=(fecha_inicio, fecha_final))\
        .values('inventario_id', 'articulo')\
        .annotate(cantidad_total=Sum('cantidad'))\
        .order_by('-cantidad_total')

    datos_json = json.dumps(list(facturas), default=str)

    return render(request, 'consulta/venta.html', {'username': request.user.username, 'user_type': request.user.user_type, 'datos': datos_json})
