from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 'client':
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_denied(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 'employee':
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view