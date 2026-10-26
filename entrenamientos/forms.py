from django import forms

from .models import Ejercicio


class EjercicioForm(forms.ModelForm):

    class Meta:
        model = Ejercicio
        fields = (
            "nombre",
            "grupo_muscular",
            "descripcion",
            "instrucciones",
            "equipo",
            "dificultad",
            "imagen",
            "video",
            "activo",
        )
        labels = {
            "nombre": "Nombre del ejercicio",
            "grupo_muscular": "Grupo muscular",
            "descripcion": "Descripción",
            "instrucciones": "Instrucciones",
            "equipo": "Equipo necesario",
            "dificultad": "Dificultad",
            "imagen": "Imagen",
            "video": "Enlace del video",
            "activo": "Ejercicio activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "grupo_muscular": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "instrucciones": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "equipo": forms.TextInput(attrs={"class": "form-control"}),
            "dificultad": forms.Select(attrs={"class": "form-control"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "video": forms.URLInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
