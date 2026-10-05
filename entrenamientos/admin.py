from django.contrib import admin

from .models import (
    Ejercicio,
    Rutina,
    RutinaEjercicio,
    AsignacionRutina,
)


admin.site.register(Ejercicio)

admin.site.register(Rutina)

admin.site.register(RutinaEjercicio)

admin.site.register(AsignacionRutina)