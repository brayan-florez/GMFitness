from common.crud import crud_patterns

from .models import Beneficio, Membresia, PlanBeneficio, PlanMembresia, PlanPrecio


urlpatterns = []

urlpatterns += crud_patterns(
    PlanMembresia,
    "planes_membresia",
    "Planes de membresía",
    route="planes-membresia",
    search_fields=("nombre", "descripcion", "sede__nombre"),
    display_fields=("nombre", "sede", "nivel_display", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    Beneficio,
    "beneficios",
    "Beneficios",
    route="beneficios",
    search_fields=("nombre", "descripcion"),
    display_fields=("nombre", "descripcion", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    PlanBeneficio,
    "planes_beneficios",
    "Beneficios por plan",
    route="planes-beneficios",
    search_fields=("plan__nombre", "beneficio__nombre"),
    display_fields=("plan", "beneficio", "detalle"),
)

urlpatterns += crud_patterns(
    PlanPrecio,
    "precios_planes",
    "Precios de planes",
    route="precios-planes",
    search_fields=("plan__nombre",),
    display_fields=("plan", "periodicidad_display", "precio", "duracion_dias", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    Membresia,
    "membresias",
    "Membresías de clientes",
    route="membresias",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido", "plan_precio__plan__nombre"),
    display_fields=("cliente", "plan_precio", "sede", "fecha_inicio", "fecha_fin", "estado_display", "precio_pagado"),
    soft_delete_field="estado",
    soft_delete_value="CANCELADA",
    delete_label="Cancelar membresía",
)
