from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import Factura, Pago


@admin.action(description="Aprobar pagos pendientes y emitir recibos")
def aprobar_pagos(modeladmin, request, queryset):
    aprobados = 0
    for pago in queryset:
        try:
            pago.aprobar()
            aprobados += 1
        except ValidationError as error:
            modeladmin.message_user(request, str(error), level=messages.ERROR)
    if aprobados:
        modeladmin.message_user(
            request,
            f"Se aprobaron {aprobados} pagos y se emitieron sus recibos.",
            level=messages.SUCCESS,
        )


@admin.action(description="Rechazar pagos pendientes")
def rechazar_pagos(modeladmin, request, queryset):
    rechazados = queryset.filter(estado="PENDIENTE").update(estado="RECHAZADO")
    modeladmin.message_user(
        request,
        f"Se rechazaron {rechazados} pagos pendientes.",
        level=messages.SUCCESS,
    )


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("membresia", "fecha_pago", "monto", "metodo_pago", "estado", "referencia")
    list_filter = ("estado", "metodo_pago", "fecha_pago")
    search_fields = ("referencia", "membresia__cliente__usuario__nombre", "membresia__cliente__usuario__apellido")
    readonly_fields = ("estado",)
    actions = (aprobar_pagos, rechazar_pagos)


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("numero", "pago", "fecha_emision", "subtotal", "total")
    search_fields = ("numero", "pago__referencia")
    readonly_fields = ("numero",)
