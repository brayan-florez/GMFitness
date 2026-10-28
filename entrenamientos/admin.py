from django.contrib import admin

from .models import (
    AsignacionRutina,
    Ejercicio,
    EjercicioEquipamiento,
    Equipamiento,
    EjercicioRealizado,
    GrupoMuscular,
    Rutina,
    RutinaDia,
    RutinaEjercicio,
    SerieRealizada,
    SesionEntrenamiento,
)


class EjercicioEquipamientoInline(admin.TabularInline):
    model = EjercicioEquipamiento
    extra = 1


class RutinaDiaInline(admin.TabularInline):
    model = RutinaDia
    extra = 1


class SerieRealizadaInline(admin.TabularInline):
    model = SerieRealizada
    extra = 1


class EjercicioRealizadoInline(admin.TabularInline):
    model = EjercicioRealizado
    extra = 1


@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Equipamiento)
class EquipamientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "grupo", "dificultad", "sede", "activo")
    list_filter = ("grupo", "dificultad", "sede", "activo")
    search_fields = ("nombre", "grupo__nombre", "descripcion")
    inlines = (EjercicioEquipamientoInline,)


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nivel", "sede", "es_predefinida", "es_publica", "activo")
    list_filter = ("nivel", "sede", "es_predefinida", "es_publica", "activo")
    search_fields = ("nombre", "descripcion")
    inlines = (RutinaDiaInline,)


@admin.register(RutinaDia)
class RutinaDiaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rutina", "dia_semana", "orden")
    list_filter = ("dia_semana",)
    search_fields = ("nombre", "rutina__nombre")


@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display = ("rutina_dia", "ejercicio", "orden", "series", "repeticiones")
    list_filter = ("rutina_dia__rutina", "ejercicio__grupo")
    search_fields = ("ejercicio__nombre", "rutina_dia__rutina__nombre")


@admin.register(AsignacionRutina)
class AsignacionRutinaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "rutina", "asignada_por", "fecha_inicio", "fecha_fin", "estado")
    list_filter = ("estado", "fecha_inicio")
    search_fields = ("cliente__usuario__nombre", "cliente__usuario__apellido", "rutina__nombre")


@admin.register(SesionEntrenamiento)
class SesionEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "fecha", "hora_inicio", "duracion_minutos")
    list_filter = ("fecha",)
    search_fields = ("cliente__usuario__nombre", "cliente__usuario__apellido")
    inlines = (EjercicioRealizadoInline,)


@admin.register(EjercicioRealizado)
class EjercicioRealizadoAdmin(admin.ModelAdmin):
    list_display = ("sesion", "ejercicio", "orden", "dificultad_percibida")
    search_fields = ("ejercicio__nombre", "sesion__cliente__usuario__nombre")
    inlines = (SerieRealizadaInline,)


@admin.register(SerieRealizada)
class SerieRealizadaAdmin(admin.ModelAdmin):
    list_display = ("ejercicio_realizado", "numero_serie", "repeticiones", "peso_utilizado")
