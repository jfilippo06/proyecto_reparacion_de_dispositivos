from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def home(request):
    return HttpResponse(f"Bienvenido {request.user.usernames} a la pagina principal")