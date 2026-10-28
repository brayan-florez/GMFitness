from django.contrib import admin

from .models import Beneficio, Membresia, PlanBeneficio, PlanMembresia, PlanPrecio


class PlanBeneficioInline(admin.TabularInline):
    model = PlanBeneficio
    extra = 1


class PlanPrecioInline(admin.TabularInline):
    model = PlanPrecio
    extra = 1


@admin.register(PlanMembresia)
class PlanMembresiaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sede", "nivel", "activo")
    list_filter = ("sede", "nivel", "activo")
    search_fields = ("nombre", "descripcion")
    inlines = (PlanBeneficioInline, PlanPrecioInline)


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "descripcion")


@admin.register(PlanPrecio)
class PlanPrecioAdmin(admin.ModelAdmin):
    list_display = ("plan", "periodicidad", "precio", "duracion_dias", "activo")
    list_filter = ("periodicidad", "activo", "plan__sede")
    search_fields = ("plan__nombre",)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "plan_precio", "sede", "fecha_inicio", "fecha_fin", "estado", "precio_pagado")
    list_filter = ("estado", "sede", "fecha_inicio")
    search_fields = ("cliente__usuario__nombre", "cliente__usuario__apellido", "plan_precio__plan__nombre")
