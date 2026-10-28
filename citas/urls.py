from common.crud import crud_patterns

from .models import Cita, DisponibilidadFisioterapeuta


urlpatterns = crud_patterns(
    DisponibilidadFisioterapeuta,
    "disponibilidades_fisioterapia",
    "Disponibilidades de fisioterapia",
    route="disponibilidades-fisioterapia",
    search_fields=("fisioterapeuta__usuario__nombre", "fisioterapeuta__usuario__apellido", "sede__nombre"),
    display_fields=("fisioterapeuta", "sede", "fecha", "hora_inicio", "hora_fin", "estado_display"),
    exclude=("estado",),
)

urlpatterns += crud_patterns(
    Cita,
    "citas",
    "Citas de fisioterapia",
    route="citas",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido", "disponibilidad__fisioterapeuta__usuario__nombre"),
    display_fields=("cliente", "disponibilidad", "fecha_reserva", "estado_display", "motivo"),
    exclude=("fecha_reserva",),
)
