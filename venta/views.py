from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
from venta.models import Client, N_Recibo, T_Lista, Factura, Totales
from inventario.models import Inventario
from configuracion.models import Impuesto
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io


# Create your views here.


def impuesto():
    impuesto = Impuesto.objects.get(id=1)
    return impuesto.is_active


def get_last_n_factura():
    last_n_recibo = N_Recibo.objects.latest('id')
    last_n_factura = last_n_recibo.n_recibo
    return last_n_factura + 1


def suma_total(request):
    last = request.session['last']
    total = T_Lista.objects.filter(n_recibo_id=last).aggregate(
        total=Sum('total'))['total']
    return total if total is not None else 0


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
    is_active = impuesto()
    sub_total = suma_total(request)
    iva = 0
    if is_active:
        i = float(Impuesto.objects.get(id=1).valor)
        iva = sub_total * i
    total = sub_total + iva
    request.session['sub_total'] = sub_total
    request.session['iva'] = iva
    request.session['total'] = total
    return render(request, 'venta/facturar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj, 'lista': registro, 'sub_total': sub_total, 'iva': iva, 'total': total, 'is_active': is_active})


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


@admin_required
@employee_denied
def cancelar_articulo(request, id):
    objeto = get_object_or_404(T_Lista, id=id)
    objeto.delete()
    return redirect('facturar_cliente')


@admin_required
@employee_denied
def cancelar_compra(request):
    last = request.session['last']
    T_Lista.objects.filter(n_recibo_id=last).delete()
    return redirect('cliente')


def registrar_factura(request):
    last = request.session['last']
    objeto = T_Lista.objects.filter(n_recibo_id=last)

    for articulo in objeto:
        registro = Factura.objects.create(
            articulo=articulo.articulo,
            cantidad=articulo.cantidad,
            costo_unidad=articulo.costo_unidad,
            total=articulo.total,
            inventario_id=articulo.inventario_id,
            n_recibo_id=last
        )
        registro.save()


def registrar_totales(request):
    last = request.session['last']
    sub_total = request.session['sub_total']
    iva = request.session['iva']
    total = request.session['total']
    totales = Totales.objects.create(
        sub_total=sub_total, iva=iva, total=total, n_recibo_id=last)
    totales.save()


def restar_inventario(request):
    last = request.session['last']
    objetos = T_Lista.objects.filter(n_recibo_id=last)

    for objeto in objetos:
        try:
            inventario = Inventario.objects.get(id=objeto.inventario_id)
        except Inventario.DoesNotExist:
            print(f"No se encontró el inventario para el objeto {objeto.id}")
            return redirect('facturar_cliente')

        inventario.cantidad -= objeto.cantidad
        inventario.save()


def contexto(request):
    last = request.session['last']
    registro = T_Lista.objects.filter(n_recibo_id=last)
    total = request.session['total']
    cedula = request.session['cedula']
    cliente = Client.objects.get(cedula=cedula)
    nombre = cliente.username
    ci = cliente.cedula
    ahora = datetime.datetime.now()
    fecha_formateada = ahora.strftime("%d/%m/%Y")
    contexto = {'listas': registro,
                'total': total,
                'usuario': request.user.username,
                'cliente': nombre,
                'cedula': ci,
                'n_recibo': last,
                'fecha': fecha_formateada, }
    return contexto


def contexto_iva(request):
    last = request.session['last']
    registro = T_Lista.objects.filter(n_recibo_id=last)
    sub_total = request.session['sub_total']
    iva = request.session['iva']
    total = request.session['total']
    cedula = request.session['cedula']
    cliente = Client.objects.get(cedula=cedula)
    nombre = cliente.username
    ci = cliente.cedula
    ahora = datetime.datetime.now()
    fecha_formateada = ahora.strftime("%d/%m/%Y")
    nombre_iva = Impuesto.objects.all()
    contexto = {'listas': registro,
                'sub_total': sub_total,
                'nombre_iva': nombre_iva,
                'iva': iva,
                'total': total,
                'usuario': request.user.username,
                'cliente': nombre,
                'cedula': ci,
                'n_recibo': last,
                'fecha': fecha_formateada, }
    return contexto


def some_view(request):
    contexto_dict = contexto(request)
    listas = contexto_dict['listas']
    total = contexto_dict['total']
    usuario = contexto_dict['usuario']
    cliente = contexto_dict['cliente']
    cedula = contexto_dict['cedula']
    n_recibo = contexto_dict['n_recibo']
    fecha = contexto_dict['fecha']

    # Crea un objeto de archivo en memoria
    buffer = io.BytesIO()

    # Crea el archivo PDF usando ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72)

    # Contenedor para los elementos 'Flowable'
    elements = []

    # Usa un estilo predeterminado y agrega algunos elementos
    styles = getSampleStyleSheet()

    # Modifica el estilo del título para alinearlo a la izquierda
    styles["Title"].alignment = 0  # 0 = TA_LEFT

    # Agrega un título
    title = Paragraph("Nota de entrega", styles["Title"])
    elements.append(title)

    # Agrega un párrafo
    paragraph = Paragraph(f"Fecha: {fecha}", styles["Normal"])
    elements.append(paragraph)

    recibo = Paragraph(f"Recibo N°: {n_recibo}", styles["Normal"])
    elements.append(recibo)

    name_client = Paragraph(f"Cliente: {cliente}", styles["Normal"])
    elements.append(name_client)

    id_client = Paragraph(f"C.I: {cedula}", styles["Normal"])
    elements.append(id_client)

    remitente = Paragraph(f"Remitente: {usuario}", styles["Normal"])
    elements.append(remitente)

    # Define los datos de la tabla
    data = [
        ['Descripcion', 'Cantidad', 'C/U', 'Total']
    ]

    # Agrega más registros al array
    for lista in listas:
        data.append([lista.articulo, lista.cantidad, lista.costo_unidad, lista.total])

    data.append(['','','total:', total])

    # Crea la tabla
    table = Table(data)

    # Define el estilo de la tabla
    style = TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),  # Alinea al centro la primera fila
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),  # Alinea a la izquierda el resto de las filas
        ('ALIGN', (-1,1), (-1,-1), 'CENTER'),  # Alinea al centro la última columna
        ('GRID', (0,0), (-1,-1), 1, colors.black),  # Dibuja una cuadrícula
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')  # Primera fila en negrita
    ])

    # Aplica el estilo a la tabla
    table.setStyle(style)

    # Agrega la tabla a los elementos
    elements.append(table)

    # Construye el PDF (incluyendo la tabla)
    doc.build(elements)

    # Recupera el valor del objeto de tipo 'file'.
    buffer.seek(0)
    pdf = buffer.read()

    # Guarda el PDF en un archivo en tu máquina
    with open('output.pdf', 'wb') as f:
        f.write(pdf)


@admin_required
@employee_denied
def facturar(request):
    # registrar_factura(request)
    # registrar_totales(request)
    # restar_inventario(request)
    some_view(request)
    return redirect('facturar_cliente')
