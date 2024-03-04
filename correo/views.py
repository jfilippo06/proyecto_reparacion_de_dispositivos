from django.shortcuts import render, redirect, get_object_or_404
from login.decorators import admin_required, employee_denied
from django.core.paginator import Paginator
from venta.models import Correo
from django.contrib import messages
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
