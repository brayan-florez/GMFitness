from django.contrib import admin

from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):

    form = UsuarioChangeForm

    list_display = (
        "nombre",
        "apellido",
        "correo",
        "documento",
        "rol",
        "sede",
        "activo",
    )

    list_filter = (
        "rol",
        "sexo",
        "activo",
        "sede",
    )

    search_fields = (
        "nombre",
        "apellido",
        "correo",
        "documento",
    )

    fieldsets = (
        ("Información personal", {
            "fields": (
                "nombre",
                "apellido",
                "documento",
                "fecha_nacimiento",
                "sexo",
                "telefono",
                "foto",
            )
        }),

        ("Información de acceso", {
            "fields": (
                "correo",
                "password",
            )
        }),

        ("Información del sistema", {
            "fields": (
                "rol",
                "sede",
                "activo",
            )
        }),
    )

    add_fieldsets = (
        ("Información personal", {
            "fields": (
                "nombre",
                "apellido",
                "documento",
                "fecha_nacimiento",
                "sexo",
                "telefono",
                "foto",
            )
        }),

        ("Información de acceso", {
            "fields": (
                "correo",
                "password1",
                "password2",
            )
        }),

        ("Información del sistema", {
            "fields": (
                "rol",
                "sede",
                "activo",
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):

        if obj is None:
            kwargs["form"] = UsuarioCreationForm
        else:
            kwargs["form"] = UsuarioChangeForm

        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):

        if obj is None:
            return self.add_fieldsets

        return self.fieldsets