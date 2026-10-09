
from django.contrib import admin
from django.db import transaction

from .models import Entrenador, Nutricionista, Fisioterapeuta
from .forms import (
    EntrenadorCreationForm,
    NutricionistaCreationForm,
    FisioterapeutaCreationForm,
)
from usuarios.models import Usuario


class ProfesionalAdminBase(admin.ModelAdmin):

    list_display = (
        "usuario",
        "especialidad",
        "experiencia",
        "activo",
    )

    search_fields = (
        "usuario__nombre",
        "usuario__apellido",
        "usuario__correo",
        "usuario__documento",
    )

    list_filter = ("activo",)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = self.formulario_creacion

        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                ("Datos personales", {
                    "fields": (
                        "nombre",
                        "apellido",
                        "documento",
                        "fecha_nacimiento",
                        "sexo",
                        "telefono",
                        "correo",
                        "foto",
                        "sede",
                    )
                }),
                ("Datos de acceso", {
                    "fields": ("password1", "password2")
                }),
                ("Información profesional", {
                    "fields": self.campos_profesionales
                }),
            )

        return super().get_fieldsets(request, obj)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not change:
            datos = form.cleaned_data

            usuario = Usuario(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                documento=datos["documento"],
                fecha_nacimiento=datos["fecha_nacimiento"],
                sexo=datos["sexo"],
                telefono=datos["telefono"],
                correo=datos["correo"],
                foto=datos.get("foto"),
                rol=self.rol_usuario,
                sede=datos["sede"],
                activo=datos.get("activo", True),
            )

            usuario.establecer_password(datos["password1"])
            usuario.save()

            obj.usuario = usuario

        super().save_model(request, obj, form, change)


@admin.register(Entrenador)
class EntrenadorAdmin(ProfesionalAdminBase):
    formulario_creacion = EntrenadorCreationForm
    rol_usuario = "ENTRENADOR"

    campos_profesionales = (
        "especialidad",
        "experiencia",
        "descripcion",
        "activo",
    )


@admin.register(Nutricionista)
class NutricionistaAdmin(ProfesionalAdminBase):
    formulario_creacion = NutricionistaCreationForm
    rol_usuario = "NUTRICIONISTA"

    campos_profesionales = (
        "especialidad",
        "registro_profesional",
        "experiencia",
        "descripcion",
        "activo",
    )


@admin.register(Fisioterapeuta)
class FisioterapeutaAdmin(ProfesionalAdminBase):
    formulario_creacion = FisioterapeutaCreationForm
    rol_usuario = "FISIOTERAPEUTA"

    campos_profesionales = (
        "especialidad",
        "registro_profesional",
        "experiencia",
        "descripcion",
        "activo",
    )