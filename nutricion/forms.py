from django import forms

from .models import Alimento


class AlimentoForm(forms.ModelForm):

    class Meta:
        model = Alimento
        fields = ("nombre", "descripcion", "activo")
        labels = {
            "nombre": "Nombre del alimento",
            "descripcion": "Descripción",
            "activo": "Alimento activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
