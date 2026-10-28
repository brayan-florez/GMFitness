from django.urls import path
from common.crud import crud_patterns
from . import views
from .models import AsignacionDieta, ComidaAlimento, ComidaDieta, Dieta

urlpatterns = [
    # CRUD de alimentos
    path('alimentos/', views.listar_alimentos, name='listar_alimentos'),
    path('alimentos/crear/', views.crear_alimento, name='crear_alimento'),
    path('alimentos/editar/<int:id>/', views.editar_alimento, name='editar_alimento'),
    path('alimentos/eliminar/<int:id>/', views.eliminar_alimento, name='eliminar_alimento'),
]

urlpatterns += crud_patterns(
    Dieta,
    "dietas",
    "Dietas",
    route="dietas",
    search_fields=("nombre", "descripcion", "creador__nombre", "creador__apellido"),
    display_fields=("nombre", "creador", "sede", "objetivo", "es_publica", "activa"),
    soft_delete_field="activa",
)

urlpatterns += crud_patterns(
    ComidaDieta,
    "comidas_dieta",
    "Comidas de dieta",
    route="comidas-dieta",
    search_fields=("nombre", "dieta__nombre"),
    display_fields=("dieta", "nombre", "tipo_comida_display", "hora_recomendada", "orden"),
)

urlpatterns += crud_patterns(
    ComidaAlimento,
    "comidas_alimentos",
    "Alimentos de comidas",
    route="comidas-alimentos",
    search_fields=("comida__nombre", "comida__dieta__nombre", "alimento__nombre"),
    display_fields=("comida", "alimento", "cantidad", "unidad", "observaciones"),
)

urlpatterns += crud_patterns(
    AsignacionDieta,
    "asignaciones_dieta",
    "Asignaciones de dieta",
    route="asignaciones-dieta",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido", "dieta__nombre"),
    display_fields=("cliente", "dieta", "asignada_por", "fecha_inicio", "fecha_fin", "estado_display"),
    soft_delete_field="estado",
    soft_delete_value="CANCELADA",
    delete_label="Cancelar asignación",
)
