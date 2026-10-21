from django import forms

from .models import Sede


class SedeForm(forms.ModelForm):

    class Meta:
        model = Sede

        fields = [
            "nombre",
            "direccion",
            "telefono",
            "activo"
        ]

        labels = {
            "nombre": "Nombre de la sede",
            "direccion": "Dirección",
            "telefono": "Teléfono",
            "activo": "Sede activa"
        }