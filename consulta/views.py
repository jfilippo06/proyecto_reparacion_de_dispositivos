from django.shortcuts import render
from login.decorators import admin_required, employee_denied
from inventario.models import Inventario
from django.core.paginator import Paginator

# Create your views here.

@admin_required
@employee_denied
def consultar_inventario(request):
    if request.method == 'GET':
        if 'inventario_pop' in request.session:
            inventario_pop = request.session['inventario_pop']
            inventario = Inventario.objects.filter(id__in=inventario_pop)
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
        request.session['inventario_pop'] = list(
            inventario.values_list('id', flat=True))

    paginator = Paginator(inventario, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'consulta/inventario.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})
