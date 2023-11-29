from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


@login_required
def users(request):
    if request.method == 'GET':
        return render(request, 'configuracion/usuarios.html', {'user_name': request.user.username})
