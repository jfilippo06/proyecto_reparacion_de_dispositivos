from login.decorators import admin_required, employee_denied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from login.models import UserProfile
from django.core.paginator import Paginator

# Create your views here.


@admin_required
@employee_denied
def usuarios(request):
    if request.method == 'GET':
        usuarios = UserProfile.objects.filter(
            is_active=False).exclude(user_type='super_user')
        paginator = Paginator(usuarios, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'papelera/usuarios.html', {'username': request.user.username, 'usuarios': page_obj})


@admin_required
@employee_denied
def habilitar_usuarios(request, id):
    user = get_object_or_404(UserProfile, id=id)
    user.is_active = True
    user.save()
    return redirect('papelera_usuarios')


@admin_required
@employee_denied
def buscar(request):
    username = request.POST['table_search']
    if username == '':
        return redirect('papelera_usuarios')
    user = UserProfile.objects.filter(username=username).exclude(
        user_type='super_user').exclude(is_active=True)
    return render(request, 'papelera/usuarios.html', {'username': request.user.username, 'usuarios': user})

