from django.shortcuts import render, redirect, get_object_or_404
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from venta.models import Correo
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
import requests
# Create your views here.

@admin_required
@employee_denied
def correo(request):
    if request.method == 'GET':
        correo = Correo.objects.all()
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
            lista = Correo.objects.filter(
                **{user_type+'__iexact': correo})
        paginator = Paginator(lista, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'correo/correo.html', {'username': request.user.username, 'correos': page_obj})


def enviar_correo(request, id):
    correo = Correo.objects.get(id=id)
    email = correo.email
    file_path = correo.link

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
        correo.delete()
        messages.success(request, 'Correo enviado exitosamente.')
        return redirect('correo')

    except (requests.ConnectionError, requests.Timeout) as e:
        # Si hubo un error en la solicitud, maneja la situación aquí.
        messages.error(request, 'Revise su conexión a internet, correo no enviado.')
        return redirect('correo')