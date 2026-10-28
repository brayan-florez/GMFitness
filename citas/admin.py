from django.contrib import admin

from .models import Cita, DisponibilidadFisioterapeuta


@admin.register(DisponibilidadFisioterapeuta)
class DisponibilidadFisioterapeutaAdmin(admin.ModelAdmin):
    list_display = ("fisioterapeuta", "sede", "fecha", "hora_inicio", "hora_fin", "estado")
    list_filter = ("estado", "sede", "fecha")
    search_fields = ("fisioterapeuta__usuario__nombre", "fisioterapeuta__usuario__apellido")
    date_hierarchy = "fecha"


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "disponibilidad", "estado", "fecha_reserva")
    list_filter = ("estado", "fecha_reserva")
    search_fields = ("cliente__usuario__nombre", "cliente__usuario__apellido", "motivo")

    def has_delete_permission(self, request, obj=None):
        # Cancelar conserva el historial y libera el horario correctamente.
        return False
