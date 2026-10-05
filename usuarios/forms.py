from django import forms
from .models import Usuario


class UsuarioCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario

        fields = (
            "nombre",
            "apellido",
            "documento",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "correo",
            "foto",
            "rol",
            "sede",
        )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.establecer_password(
            self.cleaned_data["password1"]
        )

        if commit:
            usuario.save()

        return usuario


class UsuarioChangeForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario

        fields = (
            "nombre",
            "apellido",
            "documento",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "correo",
            "foto",
            "rol",
            "sede",
            "activo",
        )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:

            if password1 != password2:
                raise forms.ValidationError(
                    "Las contraseñas no coinciden."
                )

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)

        password = self.cleaned_data.get("password1")

        if password:
            usuario.establecer_password(password)

        if commit:
            usuario.save()

        return usuario

