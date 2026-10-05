from django.contrib import admin

from .models import (
    Dieta,
    ComidaDieta,
    Alimento,
    ComidaAlimento,
    AsignacionDieta,
)


admin.site.register(Dieta)
admin.site.register(ComidaDieta)
admin.site.register(Alimento)
admin.site.register(ComidaAlimento)
admin.site.register(AsignacionDieta)