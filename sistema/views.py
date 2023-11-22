from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def home(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'home/index.html', {'user_name':request.user.username})