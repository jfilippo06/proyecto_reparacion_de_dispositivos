from django.shortcuts import render, redirect
from login.decorators import admin_required, employee_denied
from django.contrib import messages

# Create your views here.

@admin_required
@employee_denied
def servicio(request):
    if request.method == 'GET':
        return render(request, 'servicio/servicio.html', {'username': request.user.username})

    elif request.method == 'POST':
        pass