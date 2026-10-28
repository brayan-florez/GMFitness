from django import forms

from .models import Pago


class PagoForm(forms.ModelForm):
    """El estado y la fecha se controlan desde el flujo de aprobación."""

    class Meta:
        model = Pago
        fields = ("membresia", "monto", "metodo_pago", "referencia")
