
from django import forms
from django.db.models import Q

from .models import Cliente, MedicionFisica, Objetivo
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


class ObjetivoForm(forms.ModelForm):

    class Meta:
        model = Objetivo
        fields = ("nombre", "descripcion", "activo")
        labels = {
            "nombre": "Nombre del objetivo",
            "descripcion": "Descripción",
            "activo": "Objetivo activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ClienteProfileForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        label="Usuario del cliente",
        queryset=Usuario.objects.none(),
    )

    class Meta:
        model = Cliente
        fields = ("usuario", "objetivo", "activo")
        labels = {
            "objetivo": "Objetivo principal",
            "activo": "Cliente activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuarios = Usuario.objects.filter(rol="CLIENTE")
        if self.instance.pk:
            usuarios = usuarios.filter(
                Q(perfil_cliente__isnull=True)
                | Q(pk=self.instance.usuario_id)
            )
        else:
            usuarios = usuarios.filter(perfil_cliente__isnull=True)
        self.fields["usuario"].queryset = usuarios.order_by("apellido", "nombre")

    def clean_usuario(self):
        usuario = self.cleaned_data["usuario"]
        if usuario.rol != "CLIENTE":
            raise forms.ValidationError("El usuario seleccionado debe tener rol de cliente.")
        return usuario


class MedicionFisicaForm(forms.ModelForm):
    class Meta:
        model = MedicionFisica
        exclude = ("imc", "fecha_medicion")
        labels = {
            "cliente": "Cliente",
            "peso": "Peso (kg)",
            "altura": "Altura (m)",
            "porcentaje_grasa": "Porcentaje de grasa (%)",
            "cintura": "Cintura (cm)",
            "pecho": "Pecho (cm)",
            "brazo": "Brazo (cm)",
            "cadera": "Cadera (cm)",
            "muslo": "Muslo (cm)",
            "observaciones": "Observaciones",
        }
