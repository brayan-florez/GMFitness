from django.contrib import admin

from .models import (
    Alimento,
    AsignacionDieta,
    ComidaAlimento,
    ComidaDieta,
    Dieta,
)
from .forms import AlimentoForm


class AlimentoAdminForm(AlimentoForm):
    class Meta(AlimentoForm.Meta):
        fields = AlimentoForm.Meta.fields + ("creado_por",)


class ComidaDietaInline(admin.TabularInline):
    model = ComidaDieta
    extra = 1


class ComidaAlimentoInline(admin.TabularInline):
    model = ComidaAlimento
    extra = 1


@admin.register(Dieta)
class DietaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creador", "sede", "objetivo", "es_publica", "activa")
    list_filter = ("sede", "objetivo", "es_publica", "activa")
    search_fields = ("nombre", "descripcion")
    inlines = (ComidaDietaInline,)


@admin.register(ComidaDieta)
class ComidaDietaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "dieta", "tipo_comida", "hora_recomendada", "orden")
    list_filter = ("tipo_comida", "dieta")
    search_fields = ("nombre", "dieta__nombre")
    inlines = (ComidaAlimentoInline,)


@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    form = AlimentoAdminForm
    list_display = ("nombre", "codigo_barras", "calorias", "proteinas", "carbohidratos", "grasas", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "codigo_barras")


@admin.register(ComidaAlimento)
class ComidaAlimentoAdmin(admin.ModelAdmin):
    list_display = ("comida", "alimento", "cantidad", "unidad")
    search_fields = ("comida__nombre", "alimento__nombre")


@admin.register(AsignacionDieta)
class AsignacionDietaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "dieta", "asignada_por", "fecha_inicio", "fecha_fin", "estado")
    list_filter = ("estado", "fecha_inicio")
    search_fields = ("cliente__usuario__nombre", "cliente__usuario__apellido", "dieta__nombre")
