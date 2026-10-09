
from django import forms

from .models import Cliente
from usuarios.models import Usuario
from gimnasios.models import Sede


class ClienteCreationForm(forms.ModelForm):

    # Datos personales
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    documento = forms.CharField(label="Documento", max_length=20)

    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    sexo = forms.ChoiceField(
        label="Sexo",
        choices=Usuario.SEXOS
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=20
    )

    correo = forms.EmailField(
        label="Correo electrónico"
    )

    sede = forms.ModelChoiceField(
        label="Sede Smart Fit",
        queryset=Sede.objects.filter(activo=True),
        required=True
    )

    foto = forms.ImageField(
        label="Foto de perfil",
        required=False
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Cliente
        fields = ("objetivo", "activo")
        labels = {
            "objetivo": "Objetivo físico",
            "activo": "Cliente activo",
        }

    def clean_documento(self):
        documento = self.cleaned_data["documento"]

        if Usuario.objects.filter(documento=documento).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con este documento."
            )

        return documento

    def clean_correo(self):
        correo = self.cleaned_data["correo"]

        if Usuario.objects.filter(correo__iexact=correo).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con este correo electrónico."
            )

        return correo

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "Las contraseñas no coinciden."
            )

        return cleaned_data