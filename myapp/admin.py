from django.contrib import admin
from .models import (
    Casa,
    Perfil,
    Vehiculo,
    AreaComun,
    Reserva,
    Multa,
    IngresoSalida,
    Extranjero,
)

# Register your models here.

admin.site.register(Casa)
admin.site.register(Perfil)
admin.site.register(Vehiculo)
admin.site.register(AreaComun)
admin.site.register(Reserva)
admin.site.register(Multa)
admin.site.register(IngresoSalida)
admin.site.register(Extranjero)
