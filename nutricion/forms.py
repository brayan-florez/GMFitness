from decimal import Decimal

from django import forms

from .models import Alimento


class AlimentoForm(forms.ModelForm):
    porcion_referencia = forms.DecimalField(
        label="Cantidad de referencia",
        min_value=Decimal("0.01"),
        initial=Decimal("100.00"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    calorias = forms.DecimalField(
        label="Calorías por porción",
        min_value=Decimal("0"),
        initial=Decimal("0"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    proteinas = forms.DecimalField(
        label="Proteínas (g)", min_value=Decimal("0"), initial=Decimal("0"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    carbohidratos = forms.DecimalField(
        label="Carbohidratos (g)", min_value=Decimal("0"), initial=Decimal("0"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    grasas = forms.DecimalField(
        label="Grasas (g)", min_value=Decimal("0"), initial=Decimal("0"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    fibra = forms.DecimalField(
        label="Fibra (g)", min_value=Decimal("0"), initial=Decimal("0"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    class Meta:
        model = Alimento
        fields = (
            "nombre",
            "codigo_barras",
            "descripcion",
            "porcion_referencia",
            "unidad_porcion",
            "calorias",
            "proteinas",
            "carbohidratos",
            "grasas",
            "fibra",
            "imagen",
            "activo",
        )
        labels = {
            "nombre": "Nombre del alimento",
            "codigo_barras": "Código de barras",
            "descripcion": "Descripción",
            "porcion_referencia": "Cantidad de referencia",
            "unidad_porcion": "Unidad de referencia",
            "calorias": "Calorías por porción",
            "proteinas": "Proteínas (g)",
            "carbohidratos": "Carbohidratos (g)",
            "grasas": "Grasas (g)",
            "fibra": "Fibra (g)",
            "imagen": "Imagen",
            "activo": "Alimento activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
