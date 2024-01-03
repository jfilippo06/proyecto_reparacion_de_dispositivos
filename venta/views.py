from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


@admin_required
@employee_denied
def client(request):
    if request.method == 'GET':
        return render(request, 'venta/consultar_cliente.html', {'username': request.user.username})
    
    elif request.method == 'POST':
        pass
