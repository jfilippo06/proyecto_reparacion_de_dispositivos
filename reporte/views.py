from django.shortcuts import render

# Create your views here.

def recibo(request):
    return render(request, 'reporte/recibo.html', {'username': request.user.username, 'user_type': request.user.user_type})
