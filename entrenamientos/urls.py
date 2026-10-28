from django.urls import path
from common.crud import crud_patterns
from . import views
from .models import (
    AsignacionRutina,
    EjercicioEquipamiento,
    EjercicioRealizado,
    Equipamiento,
    GrupoMuscular,
    Rutina,
    RutinaDia,
    RutinaEjercicio,
    SerieRealizada,
    SesionEntrenamiento,
)

urlpatterns = [
    # CRUD de ejercicios
    path('ejercicios/', views.listar_ejercicios, name='listar_ejercicios'),
    path('ejercicios/crear/', views.crear_ejercicio, name='crear_ejercicio'),
    path('ejercicios/editar/<int:id>/', views.editar_ejercicio, name='editar_ejercicio'),
    path('ejercicios/eliminar/<int:id>/', views.eliminar_ejercicio, name='eliminar_ejercicio'),
]

urlpatterns += crud_patterns(
    GrupoMuscular,
    "grupos_musculares",
    "Grupos musculares",
    route="grupos-musculares",
    search_fields=("nombre", "descripcion"),
    display_fields=("nombre", "descripcion", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    Equipamiento,
    "equipamientos",
    "Equipamientos",
    route="equipamientos",
    search_fields=("nombre", "descripcion"),
    display_fields=("nombre", "descripcion", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    EjercicioEquipamiento,
    "ejercicio_equipamientos",
    "Equipamiento de ejercicios",
    route="ejercicio-equipamientos",
    search_fields=("ejercicio__nombre", "equipamiento__nombre"),
    display_fields=("ejercicio", "equipamiento"),
)

urlpatterns += crud_patterns(
    Rutina,
    "rutinas",
    "Rutinas",
    route="rutinas",
    search_fields=("nombre", "descripcion"),
    display_fields=("nombre", "sede", "nivel_display", "duracion_semanas", "es_publica", "activo"),
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    RutinaDia,
    "rutina_dias",
    "Días de rutina",
    route="dias-rutina",
    search_fields=("nombre", "rutina__nombre"),
    display_fields=("rutina", "dia_semana_display", "nombre", "orden"),
)

urlpatterns += crud_patterns(
    RutinaEjercicio,
    "rutina_ejercicios",
    "Ejercicios de rutina",
    route="ejercicios-rutina",
    search_fields=("ejercicio__nombre", "rutina_dia__rutina__nombre"),
    display_fields=("rutina_dia", "ejercicio", "series", "repeticiones", "peso_objetivo"),
)

urlpatterns += crud_patterns(
    AsignacionRutina,
    "asignaciones_rutina",
    "Asignaciones de rutina",
    route="asignaciones-rutina",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido", "rutina__nombre"),
    display_fields=("cliente", "rutina", "asignada_por", "fecha_inicio", "fecha_fin", "estado_display"),
    soft_delete_field="estado",
    soft_delete_value="CANCELADA",
    delete_label="Cancelar asignación",
)

urlpatterns += crud_patterns(
    SesionEntrenamiento,
    "sesiones_entrenamiento",
    "Sesiones de entrenamiento",
    route="sesiones-entrenamiento",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido"),
    display_fields=("cliente", "fecha", "hora_inicio", "hora_fin", "duracion_minutos"),
)

urlpatterns += crud_patterns(
    EjercicioRealizado,
    "ejercicios_realizados",
    "Ejercicios realizados",
    route="ejercicios-realizados",
    search_fields=("ejercicio__nombre", "sesion__cliente__usuario__nombre"),
    display_fields=("sesion", "ejercicio", "orden", "dificultad_percibida"),
)

urlpatterns += crud_patterns(
    SerieRealizada,
    "series_realizadas",
    "Series realizadas",
    route="series-realizadas",
    search_fields=("ejercicio_realizado__ejercicio__nombre",),
    display_fields=("ejercicio_realizado", "numero_serie", "repeticiones", "peso_utilizado", "duracion_segundos"),
)
