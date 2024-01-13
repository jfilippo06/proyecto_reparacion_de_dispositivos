from django.urls import path

from . import views

urlpatterns = [
    path("computadora/", views.computadora, name="computadora"),
    path("computadora/deshabilitar/<int:id>", views.deleteComputadora, name="deshabilitar_computadora"),
    path("computadora/actualizar/<int:id>", views.updateComputadora, name="actualizar_computadora"),
    path("computadora/cancelar/", views.cancelarComputadora, name="cancelar_computadora"),
   
    path("telefono/", views.telefono, name="telefono"),
    path("telefono/deshabilitar/<int:id>", views.deleteTelefono, name="deshabilitar_telefono"),
    path("telefono/actualizar/<int:id>", views.updateTelefono, name="actualizar_telefono"),
    path("telefono/cancelar/", views.cancelarTelefono, name="cancelar_telefono"),
    
    path("repuesto_computadora/", views.repuesto_computadora, name="repuestos_computadora"),
    path("repuesto_computadora/deshabilitar/<int:id>", views.deleteRepuestoComputadora, name="deshabilitar_repuestos_computadora"),
    path("repuesto_computadora/actualizar/<int:id>", views.updateRepuestoComputadora, name="actualizar_repuestos_computadora"),
    path("repuesto_computodora/cancelar/", views.cancelarRepuestosComputadora, name="cancelar_repuestos_computadora"),
    
    path("repuesto_telefono/", views.repuesto_telefono, name="repuestos_telefono"),
    path("repuesto_telefono/deshabilitar/<int:id>", views.deleteRepuestoTelefono, name="deshabilitar_repuestos_telefono"),
    path("repuesto_telefono/actualizar/<int:id>", views.updateRepuestoTelefono, name="actualizar_repuestos_telefono"),
    path("repuesto_telefono/", views.cancelarRepuestoTelefono, name="cancelar_repuesto_telefono"),
    
    path("accesorio/", views.acessorio, name="accesorio"),
    path("accesorio/deshabilitar/<int:id>", views.deleteAccesorio, name="deshabilitar_accesorio"),
    path("accesorio/actualizar/<int:id>", views.updateAccesorio, name="actualizar_accesorio"),
    path("accesorio/cancelar/", views.cancelarAccesorio, name="cancelar_accesorio"),
]
    