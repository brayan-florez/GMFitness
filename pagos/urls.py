from common.crud import crud_patterns

from .forms import PagoForm
from .models import Factura, Pago


urlpatterns = crud_patterns(
    Pago,
    "pagos",
    "Pagos",
    route="pagos",
    search_fields=("membresia__cliente__usuario__nombre", "membresia__cliente__usuario__apellido", "referencia"),
    display_fields=("membresia", "fecha_pago", "monto", "metodo_pago_display", "estado_display", "referencia"),
    form_class=PagoForm,
    exclude=("estado", "fecha_pago"),
    soft_delete_field="estado",
    soft_delete_value="RECHAZADO",
    delete_label="Rechazar pago",
    action={
        "method": "aprobar",
        "label": "Aprobar y emitir factura",
        "route": "aprobar",
        "condition_field": "estado",
        "condition_value": "PENDIENTE",
    },
)

urlpatterns += crud_patterns(
    Factura,
    "facturas",
    "Facturas emitidas",
    route="facturas",
    search_fields=("numero", "pago__referencia", "detalle"),
    display_fields=("numero", "pago", "fecha_emision", "subtotal", "total", "detalle"),
    read_only=True,
)
