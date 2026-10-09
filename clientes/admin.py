
from django.contrib import admin
from django.db import transaction

from .models import Cliente, Objetivo, MedicionFisica
from .forms import ClienteCreationForm
from usuarios.models import Usuario


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "nombre_completo",
        "correo",
        "documento",
        "objetivo",
        "activo",
    )

    search_fields = (
        "usuario__nombre",
        "usuario__apellido",
        "usuario__correo",
        "usuario__documento",
    )

    list_filter = ("activo", "objetivo")

    def nombre_completo(self, obj):
        return obj.usuario.__str__()

    nombre_completo.short_description = "Cliente"

    def correo(self, obj):
        return obj.usuario.correo

    correo.short_description = "Correo electrónico"

    def documento(self, obj):
        return obj.usuario.documento

    documento.short_description = "Documento"

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = ClienteCreationForm

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
                ("Información del cliente", {
                    "fields": ("objetivo", "activo")
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
                rol="CLIENTE",
                sede=datos["sede"],
                activo=datos.get("activo", True),
            )

            usuario.establecer_password(datos["password1"])
            usuario.save()

            obj.usuario = usuario

        super().save_model(request, obj, form, change)


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(MedicionFisica)
class MedicionFisicaAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "peso",
        "altura",
        "imc",
        "fecha_medicion",
    )

    search_fields = (
        "cliente__usuario__nombre",
        "cliente__usuario__apellido",
        "cliente__usuario__documento",
    )

    list_filter = ("fecha_medicion",)