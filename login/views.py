from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'login/index.html')

# Create your views here.
