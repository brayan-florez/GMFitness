from django import forms

from .models import Ejercicio, Equipamiento


class EjercicioForm(forms.ModelForm):
    equipamientos = forms.ModelMultipleChoiceField(
        label="Equipamiento necesario",
        queryset=Equipamiento.objects.filter(activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )


    class Meta:
        model = Ejercicio
        fields = (
            "nombre",
            "grupo",
            "sede",
            "descripcion",
            "instrucciones",
            "equipamientos",
            "dificultad",
            "imagen",
            "video",
            "activo",
        )
        labels = {
            "nombre": "Nombre del ejercicio",
            "grupo": "Grupo muscular",
            "sede": "Sede",
            "descripcion": "Descripción",
            "instrucciones": "Instrucciones",
            "equipamientos": "Equipamiento necesario",
            "dificultad": "Dificultad",
            "imagen": "Imagen",
            "video": "Enlace del video",
            "activo": "Ejercicio activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "grupo": forms.Select(attrs={"class": "form-control"}),
            "sede": forms.Select(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "instrucciones": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "dificultad": forms.Select(attrs={"class": "form-control"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "video": forms.URLInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        ejercicio = super().save(commit=commit)
        if commit:
            ejercicio.equipamientos.set(self.cleaned_data["equipamientos"])
        return ejercicio
