from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from correo.models import Correo_no_enviado, Correo_enviado
from venta.models import Client
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
import requests
# Create your views here.


@admin_required
@employee_denied
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

    return render(request, 'correo/correo.html', {'username': request.user.username, 'correos': page_obj})


def enviar_correo(request, id):
    correo = Correo_no_enviado.objects.get(id=id)
    cliente = correo.nombre_cliente
    cedula = correo.cedula
    email = correo.email
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
            [email]
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
@employee_denied
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

    return render(request, 'correo/correo_enviado.html', {'username': request.user.username, 'correos': page_obj})
