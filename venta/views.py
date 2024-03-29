from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from django.core.mail import EmailMessage
from venta.models import Client, N_Recibo, T_Lista, Factura, Totales, Direccion_de_factura, Cliente_atendido
from correo.models import Correo_enviado, Correo_no_enviado
from configuracion.models import Impuesto, Dolar
from inventario.models import Inventario
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime
import requests
import io
import os


# Create your views here.


def impuesto():
    impuesto = Impuesto.objects.get(id=1)
    return impuesto.is_active


def dolar_valor():
    dolar = Dolar.objects.get(id=1)
    return dolar.is_active


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
def client(request):
    if request.method == 'GET':
        return render(request, 'venta/consultar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type})

    elif request.method == 'POST':
        cedula = request.POST['cedula']
        request.session['cedula'] = cedula
        if Client.objects.filter(cedula=cedula):
            request.session['last'] = get_last_n_factura()
            return redirect('facturar_cliente')
        else:
            messages.error(request, 'Cliente no existe.')
            return redirect('cliente')


@admin_required
def cancelar(request):
    return redirect('cliente')


@admin_required
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
    nombre_iva = Impuesto.objects.get(id=1).iva
    iva = 0
    dolar_is_active = dolar_valor()
    dolar = float(Dolar.objects.get(id=1).valor)
    if is_active:
        i = float(Impuesto.objects.get(id=1).valor)
        iva = sub_total * i
    total = sub_total + iva
    dolar = 1 if dolar == 0 else dolar
    total_dolar = round(float(total / dolar), 2)
    request.session['sub_total'] = sub_total
    request.session['iva'] = iva
    request.session['total'] = total
    contexto_dict = contexto(request)
    cliente = contexto_dict['cliente']
    cedula = contexto_dict['cedula']
    return render(request, 'venta/facturar_cliente.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj, 'lista': registro, 'sub_total': sub_total, 'nombre_iva': nombre_iva, 'iva': iva, 'total': total, 'is_active': is_active, 'dolar_is_active': dolar_is_active, 'dolar': total_dolar, 'cliente': cliente, 'cedula': cedula})


@admin_required
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
            messages.error(request, 'No permitido.')
        except ObjectDoesNotExist:
            messages.success(request, 'Artículo agregado.')
            articulo = Inventario.objects.get(id=id)
            total = cantidad * articulo.costo
            last = request.session['last']
            registro = T_Lista.objects.create(
                articulo=articulo.articulo + " " + articulo.marca + " " + articulo.modelo + " " + articulo.no_serie, cantidad=cantidad, costo_unidad=articulo.costo, total=total, inventario_id=id,  n_recibo_id=last)
            registro.save()
    return redirect('facturar_cliente')


@admin_required
def cancelar_articulo(request, id):
    objeto = get_object_or_404(T_Lista, id=id)
    objeto.delete()
    messages.success(request, 'Artículo eliminado.')
    return redirect('facturar_cliente')


@admin_required
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
            n_recibo_id=last,
            fecha_creacion=articulo.fecha_creacion,
            fecha_actualizacion=articulo.fecha_actualizacion
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
    sub_total = request.session['sub_total']
    iva = request.session['iva']
    total = request.session['total']
    cedula = request.session['cedula']
    cliente = Client.objects.get(cedula=cedula)
    nombre = cliente.username
    ci = cliente.cedula
    id_cliente = cliente.id
    ahora = datetime.datetime.now()
    fecha_formateada = ahora.strftime("%d/%m/%Y")
    nombre_iva = Impuesto.objects.get(id=1).iva
    contexto = {'listas': registro,
                'sub_total': sub_total,
                'nombre_iva': nombre_iva,
                'iva': iva,
                'total': total,
                'usuario': request.user.username,
                'id_cliente': id_cliente,
                'cliente': nombre,
                'cedula': ci,
                'n_recibo': last,
                'fecha': fecha_formateada, }
    return contexto


def some_view(request):
    contexto_dict = contexto(request)
    listas = contexto_dict['listas']
    sub_total = contexto_dict['sub_total']
    nombre_iva = contexto_dict['nombre_iva']
    iva = contexto_dict['iva']
    total = contexto_dict['total']
    usuario = contexto_dict['usuario']
    id_cliente = contexto_dict['id_cliente']
    cliente = contexto_dict['cliente']
    cedula = contexto_dict['cedula']
    n_recibo = contexto_dict['n_recibo']
    fecha = contexto_dict['fecha']
    is_active = impuesto()

    # Crea un objeto de archivo en memoria
    buffer = io.BytesIO()

    # Crea el archivo PDF usando ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72, topMargin=10, bottomMargin=10)

    # Contenedor para los elementos 'Flowable'
    elements = []

    # Usa un estilo predeterminado y agrega algunos elementos
    styles = getSampleStyleSheet()

    # Modifica el estilo del título para alinearlo a la izquierda
    styles["Title"].alignment = 0  # 0 = TA_LEFT

    # Agrega la imagen
    img_path = 'inventario/static/img/dr_cell.png'
    img = Image(img_path, width=1*inch, height=1*inch)
    img.hAlign = 'RIGHT'
    img.vAlign = 'TOP'
    elements.append(img)

    # Agrega un título
    title = Paragraph("Dr. Cell", styles["Title"])
    elements.append(title)

    rif = Paragraph("RIF: XXXXXXXXX", styles["Title"])
    elements.append(rif)

    nota = Paragraph("Nota de entrega", styles["Title"])
    elements.append(nota)

    # Agrega un párrafo
    paragraph = Paragraph(f"Fecha: {fecha}", styles["Normal"])
    elements.append(paragraph)

    hora_actual = datetime.datetime.now()
    hora_formateada = hora_actual.strftime("%I:%M %p")
    hora = Paragraph(f"Hora: {hora_formateada}", styles["Normal"])
    elements.append(hora)

    recibo = Paragraph(f"Recibo N°: {n_recibo}", styles["Normal"])
    elements.append(recibo)

    name_client = Paragraph(f"Cliente: {cliente}", styles["Normal"])
    elements.append(name_client)

    id_client = Paragraph(f"C.I: {cedula}", styles["Normal"])
    elements.append(id_client)

    tecnico = Paragraph(f"Técnico: {request.user.username}", styles["Normal"])
    elements.append(tecnico)

    garantia = Paragraph("Garantía: 15 días habiles de garantía", styles["Normal"])
    elements.append(garantia)

    # Define los datos de la tabla
    data = [
        ['Descripcion', 'Cantidad', 'C/U', 'Total']
    ]

    # Agrega más registros al array
    for lista in listas:
        data.append([lista.articulo, lista.cantidad,
                    lista.costo_unidad, lista.total])

    if is_active:
        data.append(['', '', 'Sub total:', sub_total])
        data.append(['', '', nombre_iva, iva])
        data.append(['', '', 'Total:', total])
    else:
        data.append(['', '', 'Total:', total])

    # Crea la tabla
    # Ajusta el tamaño de las celdas
    table = Table(data, colWidths=[360, 60, 60, 60], rowHeights=25)

    # Define el estilo de la tabla
    style = TableStyle([
        # Alinea al centro la primera fila
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # Alinea a la izquierda el resto de las filas
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        # Alinea al centro la última columna
        ('ALIGN', (-1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Dibuja una cuadrícula
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')  # Primera fila en negrita
    ])

    # Aplica el estilo a la tabla
    table.setStyle(style)

    elements.append(Spacer(1, 20))

    # Agrega la tabla a los elementos
    elements.append(table)

    # Construye el PDF (incluyendo la tabla)
    doc.build(elements)

    # Recupera el valor del objeto de tipo 'file'.
    buffer.seek(0)
    pdf = buffer.read()

    # Crea la ruta al directorio
    dir_path = os.path.join(settings.BASE_DIR, 'venta', 'static', 'recibos')

    # Asegúrate de que el directorio exista
    os.makedirs(dir_path, exist_ok=True)

    # Crea la ruta al archivo
    file_path = os.path.join(dir_path, f'recibo_{n_recibo}.pdf')
    request.session['file_path'] = file_path

    # Guarda el PDF en el archivo
    with open(file_path, 'wb') as f:
        f.write(pdf)

    dir_path_link = 'http://127.0.0.1:8000/static/recibos'
    file_path_link = f'{dir_path_link}/recibo_{n_recibo}.pdf'

    save = Direccion_de_factura.objects.create(
        link=file_path_link, nombre_cliente=cliente, cedula=cedula, cliente_id=id_cliente, n_recibo_id=n_recibo)
    save.save()

    cliente = Cliente_atendido.objects.create(
        nombre_cliente=cliente, cedula=cedula, sub_total=sub_total, iva=iva, total=total, cliente_id=id_cliente, n_recibo_id=n_recibo)

    return file_path_link


def limpiar_compra(request):
    last = request.session['last']
    T_Lista.objects.filter(n_recibo_id=last).delete()


def sumar_n_recibo():
    i = get_last_n_factura()
    save = N_Recibo.objects.create(n_recibo=i)
    save.save()


def send_email(request):
    cedula = request.session['cedula']
    user_email = Client.objects.get(cedula=cedula).email
    file_path = request.session['file_path']
    contexto_dict = contexto(request)
    cliente = contexto_dict['cliente']
    n_recibo = contexto_dict['n_recibo']
    id_cliente = contexto_dict['id_cliente']

    try:
        # Intenta hacer una solicitud a un sitio web confiable.
        response = requests.get('http://www.google.com', timeout=5)
        # Lanza una excepción si la respuesta no fue exitosa.
        response.raise_for_status()

        # Si la solicitud fue exitosa, procede a enviar el correo electrónico.
        email = EmailMessage(
            'Hola',
            'Aquí está el PDF que solicitaste.',
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.attach_file(file_path)
        email.send()
        correo = Correo_enviado.objects.create(nombre_cliente= cliente, cedula=cedula, n_recibo_id=n_recibo, cliente_id= id_cliente, email= user_email, link= file_path)
        correo.save()
        messages.success(request, 'Correo enviado exitosamente.')

    except (requests.ConnectionError, requests.Timeout) as e:
        # Si hubo un error en la solicitud, maneja la situación aquí.
        correo = Correo_no_enviado.objects.create(nombre_cliente= cliente, cedula=cedula, n_recibo_id=n_recibo, cliente_id= id_cliente, email= user_email, link= file_path)
        correo.save()
        messages.error(request, 'Revise su conexión a internet, correo no enviado.')

@admin_required
def facturar(request):
    registrar_factura(request)
    registrar_totales(request)
    restar_inventario(request)
    direccion = some_view(request)
    send_email(request)
    limpiar_compra(request)
    sumar_n_recibo()
    return render(request, 'venta/ver_factura.html', {'username': request.user.username, 'user_type': request.user.user_type, 'direccion': direccion})
