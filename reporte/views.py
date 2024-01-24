from django.shortcuts import render
from login.decorators import admin_required, employee_denied
from venta.models import Direccion_de_factura
from django.core.paginator import Paginator

# Create your views here.

@admin_required
@employee_denied
def recibo(request):
    direccion = Direccion_de_factura.objects.all()
    paginator = Paginator(direccion, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'reporte/recibo.html', {'username': request.user.username, 'user_type': request.user, 'reporte': page_obj})
