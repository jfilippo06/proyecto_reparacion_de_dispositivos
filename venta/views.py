from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator
from venta.models import Client, N_Recibo, T_Lista
from inventario.models import Inventario

# Create your views here.


def get_last_n_factura():
    last_n_recibo = N_Recibo.objects.latest('id')
    last_n_factura = last_n_recibo.n_recibo
    return last_n_factura + 1


@admin_required
@employee_denied
def client(request):
    if request.method == 'GET':
        return render(request, 'venta/consultar_cliente.html', {'username': request.user.username})

    elif request.method == 'POST':
        cedula = request.POST['cedula']
        request.session['cedula'] = cedula
        if Client.objects.filter(cedula=cedula):
            request.session['last'] = get_last_n_factura()
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

        request.session['last'] = get_last_n_factura()
        return redirect('facturar_cliente')


@admin_required
@employee_denied
def cancelar(request):
    return redirect('cliente')


@admin_required
@employee_denied
def facturar_cliente(request):
    if request.method == 'GET':
        if 'inventario_ids' in request.session:
            inventario_ids = request.session['inventario_ids']
            inventario = Inventario.objects.filter(id__in=inventario_ids)
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
        request.session['inventario_ids'] = list(
            inventario.values_list('id', flat=True))

    paginator = Paginator(inventario, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    last = request.session['last']
    registro = T_Lista.objects.filter(n_recibo_id=last)
    return render(request, 'venta/facturar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj, 'lista': registro})


@admin_required
@employee_denied
def agregar_articulo(request, id):
    try:
        cantidad = int(request.POST['cantidad'])
    except ValueError:
        messages.error(request, 'Introduzca una cantidad válida.')
        return redirect('facturar_cliente')

    in_cantidad = Inventario.objects.get(id=id).cantidad
    if cantidad > in_cantidad or cantidad < 1:
        messages.error(request, 'Cantidad no permitida.')
    else:
        try:
            T_Lista.objects.get(inventario_id=id)
            messages.success(request, 'No permitido.')        
        except ObjectDoesNotExist:
            messages.success(request, 'Cantidad permitida.')
            articulo = Inventario.objects.get(id=id)
            total = cantidad * articulo.costo
            last = request.session['last']
            registro = T_Lista.objects.create(
                articulo=articulo.articulo, cantidad=cantidad, costo_unidad=articulo.costo, total=total, inventario_id=id,  n_recibo_id=last)
            registro.save()
    return redirect('facturar_cliente')
