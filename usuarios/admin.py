
from django.contrib import admin

from .models import Usuario
from .forms import UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):

    form = UsuarioChangeForm
    readonly_fields = ("rol",)

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

    ordering = ("nombre", "apellido")

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

    def has_add_permission(self, request):
        return False