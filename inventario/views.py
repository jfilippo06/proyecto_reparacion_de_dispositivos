from login.decorators import admin_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from inventario.models import Inventario
from django.core.paginator import Paginator
from django.contrib import messages


@admin_required
def inventario(request):
    if request.method == 'GET':
        return render(request, 'inventario/inventario.html', {'username': request.user.username, 'user_type': request.user.user_type})
    elif request.method == 'POST':
        codigo = request.POST['codigo'].lower().capitalize()
        articulo = request.POST['articulo'].lower().capitalize()
        marca = request.POST['marca'].lower().capitalize()
        modelo = request.POST['modelo'].lower().capitalize()
        no_serie = request.POST['no_serie'].lower().capitalize()
        cantidad = request.POST['cantidad']
        costo = request.POST['costo']
        categoria = request.POST['categoria']
        try:
            Inventario.objects.get(codigo=codigo)
            messages.success(request, 'No permitido.')
        except ObjectDoesNotExist:
            Inventario.objects.create(codigo=codigo, articulo=articulo,  marca=marca, 
                                    modelo=modelo, no_serie=no_serie, cantidad=cantidad,
                                    costo=costo, categoria=categoria, is_active=True)
            messages.success(request, 'Registrado con exito')
        return redirect('inventario')


@admin_required
def computadora(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='COM').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/computadora/computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('computadora')
        else:
            computadora = Inventario.objects.filter(
                categoria='COM', **{user_type+'__iexact': inventario}).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/computadora/computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteComputadora(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('computadora')


@admin_required
def updateComputadora(request, id):
    if request.method == "GET":
        inventario = get_object_or_404(Inventario, id=id)
        if inventario.is_active == False:
            return redirect('computadora')
        return render(request, 'inventario/computadora/editar_computadora.html', {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'computadora_id': id,
            'codigo': inventario.codigo,
            'articulo': inventario.articulo,
            'marca': inventario.marca,
            'modelo': inventario.modelo,
            'no_serie': inventario.no_serie,
            'cantidad': inventario.cantidad,
            'costo': inventario.costo,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Inventario.objects.get(pk=id)
            codigo = request.POST['codigo']

            if Inventario.objects.filter(codigo=codigo).exclude(pk=id).exists():
                inventario = get_object_or_404(Inventario, id=id)
                messages.error(request, 'Codigo ya existe')
                return render(request, 'inventario/computadora/editar_computadora.html', {
                    'username': request.user.username,
                    'user_type': request.user.user_type,
                    'computadora_id': id,
                    'codigo': inventario.codigo,
                    'articulo': inventario.articulo,
                    'marca': inventario.marca,
                    'modelo': inventario.modelo,
                    'no_serie': inventario.no_serie,
                    'cantidad': inventario.cantidad,
                    'costo': inventario.costo,
                })

            # Actualiza los campos del objeto con los nuevos valores
            objeto.codigo = request.POST['codigo']
            objeto.articulo = request.POST['articulo']
            objeto.marca = request.POST['marca']
            objeto.modelo = request.POST['modelo']
            objeto.no_serie = request.POST['no_serie']
            objeto.cantidad = request.POST['cantidad']
            objeto.costo = request.POST['costo']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('computadora')
        except Inventario.DoesNotExist:
            messages.error(
                request, 'El objeto con el código especificado no existe.')
            return redirect('computadora')


@admin_required
def cancelarComputadora(request):
    return redirect('computadora')


@admin_required
def telefono(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='TEL').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/telefono/telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('telefono')
        else:
            computadora = Inventario.objects.filter(
                categoria='TEL', **{user_type+'__iexact': inventario}).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/telefono/telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteTelefono(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('telefono')


@admin_required
def updateTelefono(request, id):
    if request.method == "GET":
        inventario = get_object_or_404(Inventario, id=id)
        if inventario.is_active == False:
            return redirect('telefonos')
        return render(request, 'inventario/telefono/editar_telefono.html', {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'computadora_id': id,
            'codigo': inventario.codigo,
            'articulo': inventario.articulo,
            'marca': inventario.marca,
            'modelo': inventario.modelo,
            'no_serie': inventario.no_serie,
            'cantidad': inventario.cantidad,
            'costo': inventario.costo,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Inventario.objects.get(pk=id)
            codigo = request.POST['codigo']

            if Inventario.objects.filter(codigo=codigo).exclude(pk=id).exists():
                inventario = get_object_or_404(Inventario, id=id)
                messages.error(request, 'Codigo ya existe')
                return render(request, 'inventario/computadora/editar_telefono.html', {
                    'username': request.user.username,
                    'user_type': request.user.user_type,
                    'computadora_id': id,
                    'codigo': inventario.codigo,
                    'articulo': inventario.articulo,
                    'marca': inventario.marca,
                    'modelo': inventario.modelo,
                    'no_serie': inventario.no_serie,
                    'cantidad': inventario.cantidad,
                    'costo': inventario.costo,
                })

            # Actualiza los campos del objeto con los nuevos valores
            objeto.codigo = request.POST['codigo']
            objeto.articulo = request.POST['articulo']
            objeto.marca = request.POST['marca']
            objeto.modelo = request.POST['modelo']
            objeto.no_serie = request.POST['no_serie']
            objeto.cantidad = request.POST['cantidad']
            objeto.costo = request.POST['costo']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('telefono')
        except Inventario.DoesNotExist:
            messages.error(
                request, 'El objeto con el código especificado no existe.')
            return redirect('telefono')


@admin_required
def cancelarTelefono(request):
    return redirect('telefono')


@admin_required
def repuesto_computadora(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='RPC').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/repuesto_computadora/repuesto_computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('repuestos_computadora')
        else:
            computadora = Inventario.objects.filter(
                categoria='RPC', **{user_type+'__iexact': inventario}).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/repuesto_computadora/repuesto_computadora.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteRepuestoComputadora(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('repuestos_computadora')


@admin_required
def updateRepuestoComputadora(request, id):
    if request.method == "GET":
        inventario = get_object_or_404(Inventario, id=id)
        if inventario.is_active == False:
            return redirect('repuestos_computadora')
        return render(request, 'inventario/repuesto_computadora/editar_repuesto_computadora.html', {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'computadora_id': id,
            'codigo': inventario.codigo,
            'articulo': inventario.articulo,
            'marca': inventario.marca,
            'modelo': inventario.modelo,
            'no_serie': inventario.no_serie,
            'cantidad': inventario.cantidad,
            'costo': inventario.costo,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Inventario.objects.get(pk=id)
            codigo = request.POST['codigo']

            if Inventario.objects.filter(codigo=codigo).exclude(pk=id).exists():
                inventario = get_object_or_404(Inventario, id=id)
                messages.error(request, 'Codigo ya existe')
                return render(request, 'inventario/repuesto_computadora/editar_repuesto_computadora.html', {
                    'username': request.user.username,
                    'user_type': request.user.user_type,
                    'computadora_id': id,
                    'codigo': inventario.codigo,
                    'articulo': inventario.articulo,
                    'marca': inventario.marca,
                    'modelo': inventario.modelo,
                    'no_serie': inventario.no_serie,
                    'cantidad': inventario.cantidad,
                    'costo': inventario.costo,
                })

            # Actualiza los campos del objeto con los nuevos valores
            objeto.codigo = request.POST['codigo']
            objeto.articulo = request.POST['articulo']
            objeto.marca = request.POST['marca']
            objeto.modelo = request.POST['modelo']
            objeto.no_serie = request.POST['no_serie']
            objeto.cantidad = request.POST['cantidad']
            objeto.costo = request.POST['costo']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('repuestos_computadora')
        except Inventario.DoesNotExist:
            messages.error(
                request, 'El objeto con el código especificado no existe.')
            return redirect('repuestos_computadora')


@admin_required
def cancelarRepuestosComputadora(request):
    return redirect('repuestos_computadora')


@admin_required
def repuesto_telefono(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='RPT').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/repuesto_telefono/repuesto_telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('repuestos_telefono')
        else:
            computadora = Inventario.objects.filter(
                categoria='RPT', **{user_type+'__iexact': inventario}).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/repuesto_telefono/repuesto_telefono.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteRepuestoTelefono(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('repuestos_telefono')


@admin_required
def updateRepuestoTelefono(request, id):
    if request.method == "GET":
        inventario = get_object_or_404(Inventario, id=id)
        if inventario.is_active == False:
            return redirect('repuestos_telefono')
        return render(request, 'inventario/repuesto_telefono/editar_repuesto_telefono.html', {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'computadora_id': id,
            'codigo': inventario.codigo,
            'articulo': inventario.articulo,
            'marca': inventario.marca,
            'modelo': inventario.modelo,
            'no_serie': inventario.no_serie,
            'cantidad': inventario.cantidad,
            'costo': inventario.costo,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Inventario.objects.get(pk=id)
            codigo = request.POST['codigo']

            if Inventario.objects.filter(codigo=codigo).exclude(pk=id).exists():
                inventario = get_object_or_404(Inventario, id=id)
                messages.error(request, 'Codigo ya existe')
                return render(request, 'inventario/repuesto_telefono/editar_repuesto_telefono.html', {
                    'username': request.user.username,
                    'user_type': request.user.user_type,
                    'computadora_id': id,
                    'codigo': inventario.codigo,
                    'articulo': inventario.articulo,
                    'marca': inventario.marca,
                    'modelo': inventario.modelo,
                    'no_serie': inventario.no_serie,
                    'cantidad': inventario.cantidad,
                    'costo': inventario.costo,
                })

            # Actualiza los campos del objeto con los nuevos valores
            objeto.codigo = request.POST['codigo']
            objeto.articulo = request.POST['articulo']
            objeto.marca = request.POST['marca']
            objeto.modelo = request.POST['modelo']
            objeto.no_serie = request.POST['no_serie']
            objeto.cantidad = request.POST['cantidad']
            objeto.costo = request.POST['costo']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('repuestos_telefono')
        except Inventario.DoesNotExist:
            messages.error(
                request, 'El objeto con el código especificado no existe.')
            return redirect('repuestos_telefono')


@admin_required
def cancelarRepuestoTelefono(request):
    return redirect('repuestos_telefono')


@admin_required
def acessorio(request):
    if request.method == 'GET':
        inventario = Inventario.objects.filter(
            categoria='ASE').exclude(is_active=False)
        paginator = Paginator(inventario, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/accesorio/accesorio.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})

    elif request.method == 'POST':
        inventario = request.POST['table_search']
        user_type = request.POST['user_type']
        if inventario == '':
            return redirect('accesorio')
        else:
            computadora = Inventario.objects.filter(
                categoria='ASE', **{user_type+'__iexact': inventario}).exclude(is_active=False)
        paginator = Paginator(computadora, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventario/accesorio/accesorio.html', {'username': request.user.username, 'user_type': request.user.user_type, 'inventario': page_obj})


@admin_required
def deleteAccesorio(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.is_active = False
    inventario.save()
    return redirect('accesorio')


@admin_required
def updateAccesorio(request, id):
    if request.method == "GET":
        inventario = get_object_or_404(Inventario, id=id)
        if inventario.is_active == False:
            return redirect('repuestos_telefono')
        return render(request, 'inventario/accesorio/editar_accesorio.html', {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'computadora_id': id,
            'codigo': inventario.codigo,
            'articulo': inventario.articulo,
            'marca': inventario.marca,
            'modelo': inventario.modelo,
            'no_serie': inventario.no_serie,
            'cantidad': inventario.cantidad,
            'costo': inventario.costo,
        })

    elif request.method == "POST":
        try:
            # Obtén el objeto que quieres actualizar
            objeto = Inventario.objects.get(pk=id)
            codigo = request.POST['codigo']

            if Inventario.objects.filter(codigo=codigo).exclude(pk=id).exists():
                inventario = get_object_or_404(Inventario, id=id)
                messages.error(request, 'Codigo ya existe')
                return render(request, 'inventario/accesorio/editar_accesorio.html', {
                    'username': request.user.username,
                    'user_type': request.user.user_type,
                    'computadora_id': id,
                    'codigo': inventario.codigo,
                    'articulo': inventario.articulo,
                    'marca': inventario.marca,
                    'modelo': inventario.modelo,
                    'no_serie': inventario.no_serie,
                    'cantidad': inventario.cantidad,
                    'costo': inventario.costo,
                })

            # Actualiza los campos del objeto con los nuevos valores
            objeto.codigo = request.POST['codigo']
            objeto.articulo = request.POST['articulo']
            objeto.marca = request.POST['marca']
            objeto.modelo = request.POST['modelo']
            objeto.no_serie = request.POST['no_serie']
            objeto.cantidad = request.POST['cantidad']
            objeto.costo = request.POST['costo']

            # Guarda los cambios en la base de datos
            objeto.save()

            messages.error(request, 'Actualizado correctamente')
            return redirect('accesorio')
        except Inventario.DoesNotExist:
            messages.error(
                request, 'El objeto con el código especificado no existe.')
            return redirect('accesorio')


@admin_required
def cancelarAccesorio(request):
    return redirect('accesorio')
