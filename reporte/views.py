from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from venta.models import Direccion_de_factura
from inventario.models import Inventario
from django.core.paginator import Paginator
from reparacion.models import Reparacion
from venta.models import Totales, Cliente_atendido
from venta.views import impuesto
from django.db.models import Q
from datetime import datetime, time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.contrib import messages


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
            messages.error(request, 'introduzca texto.')
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
        return render(request, 'reporte/reparacion.html', {'username': request.user.username, 'reparaciones': page_obj})

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
            return render(request, 'reporte/reparacion.html', {'username': request.user.username, 'reparaciones': page_obj})
        elif 'enviar' in request.POST['submit_button']:
            if not reparaciones:
                # Redirige a otra página (por ejemplo, a 'home')
                return redirect('reporte_reparaciones')

            # Crea un objeto de archivo en memoria
            buffer = BytesIO()

            # Crea el archivo PDF usando ReportLab
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=72, leftMargin=72, topMargin=10, bottomMargin=10)

            # Contenedor para los elementos 'Flowable'
            elements = []

            # Usa un estilo predeterminado y agrega algunos elementos
            styles = getSampleStyleSheet()

            # Modifica el estilo del título para alinearlo al centro
            styles["Title"].alignment = 1  # 1 = TA_CENTER

            # Agrega la imagen
            img_path = 'inventario/static/img/dr_cell.png'
            img = Image(img_path, width=1*inch, height=1*inch)
            img.hAlign = 'RIGHT'
            img.vAlign = 'TOP'
            elements.append(img)

            # Agrega un título
            title = Paragraph("Reporte - Reparaciónes", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 10))

            fecha_b = Paragraph(f"Fecha: {date_begin}", styles["Normal"])
            elements.append(fecha_b)

            fecha_e = Paragraph(f"Fecha: {date_end}", styles["Normal"])
            elements.append(fecha_e)

            # Agrega un espacio
            elements.append(Spacer(1, 25))

            # Define los datos de la tabla
            data = [
                ['ID', 'Artículo', 'Descripción', 'Cantidad',
                    'Cliente', 'Cédula', 'Estado']
            ]

            # Agrega más registros al array
            for reparacion in reparaciones:
                data.append([reparacion.id, reparacion.articulo,
                            reparacion.descripcion, reparacion.cantidad, reparacion.username, reparacion.cedula, reparacion.estado])

            # Si la tabla se está volviendo muy larga, inserta un salto de página
            if len(data) % 25 == 0:  # ajusta el número según tus necesidades
                elements.append(
                    Table(data, colWidths=[40, 110, 200, 60, 80, 70, 40]))
                elements.append(PageBreak())
                for reparacion in reparaciones:
                    data.append([reparacion.id, reparacion.articulo,
                                 reparacion.descripcion, reparacion.cantidad, reparacion.username, reparacion.cedula, reparacion.estado])

            # Crea la tabla
            table = Table(data, colWidths=[40, 110, 200, 60, 80, 70, 40])

            # Define el estilo de la tabla
            style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Aplica el estilo a la tabla
            table.setStyle(style)

            # Agrega la tabla a los elementos
            elements.append(table)

            # Construye el PDF (incluyendo la tabla)
            doc.build(elements)

            # Recupera el valor del objeto de tipo 'file'.
            buffer.seek(0)
            pdf = buffer.getvalue()
            buffer.close()

            # Crea un archivo en memoria con el contenido del PDF
            pdf_file = ContentFile(pdf)

            response = FileResponse(
                pdf_file, as_attachment=False, filename='blank.pdf')
            response['Content-Type'] = 'application/pdf'
            return response


@admin_required
@employee_denied
def reporteCliente(request):
    if request.method == 'GET':
        cliente = Cliente_atendido.objects.all()
        paginator = Paginator(cliente, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        iva = impuesto()
        return render(request, 'reporte/cliente.html', {'username': request.user.username, 'cliente': page_obj, 'is_active': iva})

    elif request.method == 'POST':
        iva = impuesto()
        date_begin = datetime.strptime(request.POST.get('date_begin', ''), '%Y-%m-%d') if request.POST.get(
            'date_begin', '') else datetime.combine(datetime.today(), time.min)
        date_end = datetime.strptime(request.POST.get(
            'date_end', ''), '%Y-%m-%d') if request.POST.get('date_end', '') else datetime.now()
        table_search = request.POST['table_search']

        query = Q()

        if request.POST['user_type'] == 'nombre_cliente':
            if table_search:
                query &= Q(nombre_cliente=table_search)
        elif request.POST['user_type'] == 'cedula':
            if table_search:
                query &= Q(cedula=table_search)
        elif request.POST['user_type'] == 'todos':
            pass

        query &= Q(fecha_creacion__range=(date_begin, date_end))

        cliente = Cliente_atendido.objects.filter(query)

        if 'buscar' in request.POST['submit_button']:
            paginator = Paginator(cliente, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            iva = impuesto()
            return render(request, 'reporte/cliente.html', {'username': request.user.username, 'cliente': page_obj, 'is_active': iva})
        elif 'enviar' in request.POST['submit_button']:
            if not cliente:
                # Redirige a otra página (por ejemplo, a 'home')
                return redirect('reporte_cliente')

            # Crea un objeto de archivo en memoria
            buffer = BytesIO()

            # Crea el archivo PDF usando ReportLab
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=72, leftMargin=72, topMargin=10, bottomMargin=10)

            # Contenedor para los elementos 'Flowable'
            elements = []

            # Usa un estilo predeterminado y agrega algunos elementos
            styles = getSampleStyleSheet()

            # Modifica el estilo del título para alinearlo al centro
            styles["Title"].alignment = 1  # 1 = TA_CENTER

            # Agrega la imagen
            img_path = 'inventario/static/img/dr_cell.png'
            img = Image(img_path, width=1*inch, height=1*inch)
            img.hAlign = 'RIGHT'
            img.vAlign = 'TOP'
            elements.append(img)

            # Agrega un título
            title = Paragraph("Reporte - Clientes", styles["Title"])
            elements.append(title)

            fecha_b = Paragraph(f"Fecha: {date_begin}", styles["Normal"])
            elements.append(fecha_b)

            fecha_e = Paragraph(f"Fecha: {date_end}", styles["Normal"])
            elements.append(fecha_e)

            # Agrega un espacio
            elements.append(Spacer(1, 25))

            # Define los datos de la tabla
            if iva:
                data = [
                    ['ID', 'Cliente', 'Cédula', 'Sub-total',
                        'Iva', 'Total', 'N° recibo']
                ]
            else:
                data = [
                    ['ID', 'Cliente', 'Cédula', 'Total', 'N° recibo']
                ]

            # Agrega más registros al array
            if iva:
                for i in cliente:
                    data.append([i.id, i.nombre_cliente, i.cedula, i.sub_total,
                                i.iva, i.total, i.n_recibo_id])
            else:
                for i in cliente:
                    data.append([i.id, i.nombre_cliente,
                                i.cedula, i.total, i.n_recibo_id])

            # Si la tabla se está volviendo muy larga, inserta un salto de página
            if len(data) % 25 == 0:  # ajusta el número según tus necesidades
                elements.append(
                    Table(data, colWidths=[40, 70, 40, 70, 40]))
                elements.append(PageBreak())
                if iva:
                    for i in cliente:
                        data.append([i.id, i.nombre_cliente, i.cedula, i.sub_total,
                                     i.iva, i.total, i.n_recibo_id])
                else:
                    for i in cliente:
                        data.append([i.id, i.nombre_cliente,
                                    i.cedula, i.total, i.n_recibo_id])

            # Crea la tabla
            if iva:
                table = Table(data, colWidths=[40, 130, 40, 70, 70, 70, 70])
            else:
                table = Table(data, colWidths=[40, 130, 40, 70, 70])

            # Define el estilo de la tabla
            style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Aplica el estilo a la tabla
            table.setStyle(style)

            # Agrega la tabla a los elementos
            elements.append(table)

            # Construye el PDF (incluyendo la tabla)
            doc.build(elements)

            # Recupera el valor del objeto de tipo 'file'.
            buffer.seek(0)
            pdf = buffer.getvalue()
            buffer.close()

            # Crea un archivo en memoria con el contenido del PDF
            pdf_file = ContentFile(pdf)

            response = FileResponse(
                pdf_file, as_attachment=False, filename='blank.pdf')
            response['Content-Type'] = 'application/pdf'
            return response


@admin_required
@employee_denied
def reporteInventario(request):
    if request.method == 'GET':
        if 'inventario_ads' in request.session:
            inventario_ads = request.session['inventario_ads']
            inventario = Inventario.objects.filter(id__in=inventario_ads)
            paginator = Paginator(inventario, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            return render(request, 'reporte/inventario.html', {'username': request.user.username, 'inventario': page_obj})
        else:
            inventario = []
            paginator = Paginator(inventario, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            return render(request, 'reporte/inventario.html', {'username': request.user.username, 'inventario': page_obj})

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
        request.session['inventario_ads'] = list(
            inventario.values_list('id', flat=True))

        if 'buscar' in request.POST['submit_button']:
            paginator = Paginator(inventario, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            return render(request, 'reporte/inventario.html', {'username': request.user.username, 'inventario': page_obj})
        elif 'enviar' in request.POST['submit_button']:
            if not inventario:
                # Redirige a otra página (por ejemplo, a 'home')
                return redirect('reporte_inventario')

            buffer = BytesIO()

            # Crea el archivo PDF usando ReportLab
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=72, leftMargin=72, topMargin=10, bottomMargin=10)

            # Contenedor para los elementos 'Flowable'
            elements = []

            # Usa un estilo predeterminado y agrega algunos elementos
            styles = getSampleStyleSheet()

            # Modifica el estilo del título para alinearlo al centro
            styles["Title"].alignment = 1  # 1 = TA_CENTER

            # Agrega la imagen
            # Asegúrate de cambiar esto por la ruta a tu imagen
            img_path = 'inventario/static/img/dr_cell.png'
            # Cambia el tamaño según tus necesidades
            img = Image(img_path, width=1*inch, height=1*inch)
            img.hAlign = 'RIGHT'
            img.vAlign = 'TOP'
            elements.append(img)

            # Agrega un título
            title = Paragraph("Reporte - Inventario", styles["Title"])
            elements.append(title)

            # Agrega un espacio
            elements.append(Spacer(1, 25))

            # Define los datos de la tabla
            data = [
                ['ID', 'Código', 'Artículo', 'Marca',
                    'Modelo', 'N° serie', 'Cantidad', 'Costo']
            ]

            # Agrega más registros al array
            for i in inventario:
                data.append([i.id, i.codigo, i.articulo, i.marca,
                            i.modelo, i.no_serie, i.cantidad, i.costo])

            # Si la tabla se está volviendo muy larga, inserta un salto de página
            if len(data) % 25 == 0:  # ajusta el número según tus necesidades
                elements.append(
                    Table(data, colWidths=[30, 50, 100, 90, 90, 70, 60, 70]))
                elements.append(PageBreak())
                for i in inventario:
                    data.append([i.id, i.codigo, i.articulo, i.marca,
                                i.modelo, i.no_serie, i.cantidad, i.costo])

            # Crea la tabla
            table = Table(data, colWidths=[30, 50, 100, 90, 90, 70, 60, 70])

            # Define el estilo de la tabla
            style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Aplica el estilo a la tabla
            table.setStyle(style)

            # Agrega la tabla a los elementos
            elements.append(table)

            # Construye el PDF (incluyendo la tabla)
            doc.build(elements)

            # Recupera el valor del objeto de tipo 'file'.
            buffer.seek(0)
            pdf = buffer.getvalue()
            buffer.close()

            # Crea un archivo en memoria con el contenido del PDF
            pdf_file = ContentFile(pdf)

            response = FileResponse(
                pdf_file, as_attachment=False, filename='blank.pdf')
            response['Content-Type'] = 'application/pdf'
            return response


@admin_required
@employee_denied
def reporteVenta(request):
    if request.method == 'GET':
        venta = Totales.objects.all()
        paginator = Paginator(venta, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        iva = impuesto()
        return render(request, 'reporte/venta.html', {'username': request.user.username, 'ventas': page_obj, 'is_active': iva})

    elif request.method == 'POST':
        iva = impuesto()
        date_begin = datetime.strptime(request.POST.get('date_begin', ''), '%Y-%m-%d') if request.POST.get(
            'date_begin', '') else datetime.combine(datetime.today(), time.min)
        date_end = datetime.strptime(request.POST.get(
            'date_end', ''), '%Y-%m-%d') if request.POST.get('date_end', '') else datetime.now()

        query = Q()
        query &= Q(fecha_creacion__range=(date_begin, date_end))
        venta = Totales.objects.filter(query)

        if 'buscar' in request.POST['submit_button']:
            paginator = Paginator(venta, 15)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            return render(request, 'reporte/venta.html', {'username': request.user.username, 'ventas': page_obj, 'is_active': iva})
        elif 'enviar' in request.POST['submit_button']:
            if not venta:
                # Redirige a otra página (por ejemplo, a 'home')
                return redirect('reporte_venta')

            # Crea un objeto de archivo en memoria
            buffer = BytesIO()

            # Crea el archivo PDF usando ReportLab
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=72, leftMargin=72, topMargin=10, bottomMargin=10)

            # Contenedor para los elementos 'Flowable'
            elements = []

            # Usa un estilo predeterminado y agrega algunos elementos
            styles = getSampleStyleSheet()

            # Modifica el estilo del título para alinearlo al centro
            styles["Title"].alignment = 1  # 1 = TA_CENTER

            # Agrega la imagen
            img_path = 'inventario/static/img/dr_cell.png'
            img = Image(img_path, width=1*inch, height=1*inch)
            img.hAlign = 'RIGHT'
            img.vAlign = 'TOP'
            elements.append(img)

            # Agrega un título
            title = Paragraph("Reporte - Ventas", styles["Title"])
            elements.append(title)

            fecha_b = Paragraph(f"Fecha: {date_begin}", styles["Normal"])
            elements.append(fecha_b)

            fecha_e = Paragraph(f"Fecha: {date_end}", styles["Normal"])
            elements.append(fecha_e)

            # Agrega un espacio
            elements.append(Spacer(1, 25))

            # Define los datos de la tabla
            if iva:
                data = [
                    ['ID', 'Sub total', 'Iva', 'Total', 'N° recibo']
                ]
            else:
                data = [
                    ['ID', 'Total', 'N° recibo']
                ]

            # Agrega más registros al array
            if iva:
                for i in venta:
                    data.append([i.id, i.sub_total, i.iva,
                                i.total, i.n_recibo_id])
            else:
                for i in venta:
                    data.append([i.id, i.total, i.n_recibo_id])

            # Si la tabla se está volviendo muy larga, inserta un salto de página
            if len(data) % 25 == 0:  # ajusta el número según tus necesidades
                elements.append(
                    Table(data, colWidths=[100, 100, 100]))
                elements.append(PageBreak())
                if iva:
                    for i in venta:
                        data.append([i.id, i.sub_total, i.iva,
                                    i.total, i.n_recibo_id])
                else:
                    for i in venta:
                        data.append([i.id, i.total, i.n_recibo_id])

            # Crea la tabla
            table = Table(data, colWidths=[100, 100, 100])

            # Define el estilo de la tabla
            style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Aplica el estilo a la tabla
            table.setStyle(style)

            # Agrega la tabla a los elementos
            elements.append(table)

            # Construye el PDF (incluyendo la tabla)
            doc.build(elements)

            # Recupera el valor del objeto de tipo 'file'.
            buffer.seek(0)
            pdf = buffer.getvalue()
            buffer.close()

            # Crea un archivo en memoria con el contenido del PDF
            pdf_file = ContentFile(pdf)

            response = FileResponse(
                pdf_file, as_attachment=False, filename='blank.pdf')
            response['Content-Type'] = 'application/pdf'
            return response
