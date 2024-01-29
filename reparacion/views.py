from django.shortcuts import render

# Create your views here.

def reparacion(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'reparacion/reparacion.html', {'username': request.user.username})