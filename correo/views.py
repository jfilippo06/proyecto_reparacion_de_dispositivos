from django.shortcuts import render, redirect
from login.decorators import admin_required
from django.core.paginator import Paginator
from correo.models import Correo_no_enviado, Correo_enviado
from venta.models import Client
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
import requests
import os
# Create your views here.


@admin_required
def correo(request):
    if request.method == 'GET':
        correo = Correo_no_enviado.objects.all()
        paginator = Paginator(correo, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        correo = request.POST['table_search']
        user_type = request.POST['user_type']
        if correo == '':
            messages.error(request, 'Introduzca texto.')
            return redirect('correo')
        else:
            lista = Correo_no_enviado.objects.filter(
                **{user_type+'__iexact': correo})
        paginator = Paginator(lista, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'correo/correo.html', {'username': request.user.username, 'user_type': request.user.user_type, 'correos': page_obj})


@admin_required
def enviar_correo(request, id):
    correo = Correo_no_enviado.objects.get(id=id)
    cliente = correo.nombre_cliente
    cedula = correo.cedula
    email_correo = correo.email
    user_email = Client.objects.get(cedula=cedula).email
    file_path = correo.link
    n_recibo = correo.n_recibo_id
    id_cliente = correo.cliente_id

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
            [email_correo]
        )
        email.attach_file(file_path)
        email.send()
        enviar = Correo_enviado.objects.create(
            nombre_cliente=cliente, cedula=cedula, email=user_email, n_recibo_id=n_recibo, cliente_id=id_cliente, link=file_path)
        enviar.save()
        correo.delete()
        messages.success(request, 'Correo enviado exitosamente.')
        return redirect('correo_no_enviado')

    except (requests.ConnectionError, requests.Timeout) as e:
        # Si hubo un error en la solicitud, maneja la situación aquí.
        messages.error(
            request, 'Revise su conexión a internet, correo no enviado.')
        return redirect('correo_no_enviado')


@admin_required
def correo_enviado(request):
    if request.method == 'GET':
        correo = Correo_enviado.objects.all().order_by('-id')
        paginator = Paginator(correo, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    elif request.method == 'POST':
        correo = request.POST['table_search']
        user_type = request.POST['user_type']
        if correo == '':
            messages.error(request, 'Introduzca texto.')
            return redirect('correo_enviado')
        else:
            lista = Correo_enviado.objects.filter(
                **{user_type+'__iexact': correo})
        paginator = Paginator(lista, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'correo/correo_enviado.html', {'username': request.user.username, 'user_type': request.user.user_type, 'correos': page_obj})


def handle_uploaded_file(f):
    dir_path = os.path.join(settings.BASE_DIR, 'correo', 'static', 'archivos',)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f.name)  # Aquí está el cambio
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


@admin_required
def crear_correo(request):
    if request.method == 'GET':
        return render(request, 'correo/crear_correo.html', {'username': request.user.username, 'user_type': request.user.user_type,})

    elif request.method == 'POST':
        correo = request.POST['correo']
        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje']

        try:
            # Intenta hacer una solicitud a un sitio web confiable.
            response = requests.get('http://www.google.com', timeout=5)
            # Lanza una excepción si la respuesta no fue exitosa.
            response.raise_for_status()

            if 'archivo' in request.FILES:
                archivo = request.FILES['archivo']
                file_path = handle_uploaded_file(archivo)
            else:
                messages.error(request, 'No se subió ningún archivo.')
                return redirect('crear_correo')

            # Si la solicitud fue exitosa, procede a enviar el correo electrónico.
            email = EmailMessage(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [correo]
            )
            email.attach_file(file_path)
            email.send()
            messages.success(request, 'Correo enviado exitosamente.')
            return redirect('crear_correo')

        except (requests.ConnectionError, requests.Timeout) as e:
            # Si hubo un error en la solicitud, maneja la situación aquí.
            messages.error(
                request, 'Revise su conexión a internet, correo no enviado.')
            return redirect('crear_correo')


@admin_required
def enviar_todo(request):
    correos = Correo_no_enviado.objects.all()
    try:
        # Intenta hacer una solicitud a un sitio web confiable.
        response = requests.get('http://www.google.com', timeout=5)
        # Lanza una excepción si la respuesta no fue exitosa.
        response.raise_for_status()

        # Si la solicitud fue exitosa, procede a enviar el correo electrónico.
        for correo in correos:
            email = EmailMessage(
                'Hola',
                'Aquí está el PDF que solicitaste.',
                settings.EMAIL_HOST_USER,
                [correo.email]
            )
            email.attach_file(correo.link)
            email.send()
            enviar = Correo_enviado.objects.create(
                nombre_cliente=correo.nombre_cliente, cedula=correo.cedula, email=correo.email, n_recibo_id=correo.n_recibo_id, cliente_id=correo.cliente_id, link=correo.link)
            enviar.save()

        correos.delete()
        messages.success(request, 'Correos enviados exitosamente.')
        return redirect('correo_no_enviado')

    except (requests.ConnectionError, requests.Timeout) as e:
        # Si hubo un error en la solicitud, maneja la situación aquí.
        messages.error(
            request, 'Revise su conexión a internet, correos no enviados.')
        return redirect('correo_no_enviado')
