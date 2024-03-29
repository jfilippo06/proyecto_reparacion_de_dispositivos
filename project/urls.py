"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('inventario/', include('inventario.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('papelera/', include('papelera.urls')),
    path('venta/', include('venta.urls')),
    path('reporte/', include('reporte.urls')),
    path('mantenimiento/', include('mantenimiento.urls')),
    path('reparacion/', include('reparacion.urls')),
    path('cliente/', include('cliente.urls')),
    path('consulta/', include('consulta.urls')),
    path('correo/', include('correo.urls')),
]
