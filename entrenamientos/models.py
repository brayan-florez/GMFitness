from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ("nombre",)

    def __str__(self):
        return self.nombre


class Equipamiento(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ("nombre",)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    DIFICULTADES = [
        ("BASICO", "Básico"),
        ("INTERMEDIO", "Intermedio"),
        ("AVANZADO", "Avanzado"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    grupo = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.PROTECT,
        related_name="ejercicios",
    )
    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ejercicios",
    )
    creado_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ejercicios_creados",
    )
    descripcion = models.TextField(blank=True)
    instrucciones = models.TextField(blank=True)
    dificultad = models.CharField(
        max_length=20,
        choices=DIFICULTADES,
        default="BASICO",
    )
    equipamientos = models.ManyToManyField(
        Equipamiento,
        through="EjercicioEquipamiento",
        related_name="ejercicios",
        blank=True,
    )
    imagen = models.ImageField(upload_to="ejercicios/", blank=True, null=True)
    video = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("nombre",)

    def clean(self):
        if self.creado_por_id and self.creado_por.rol not in {"ENTRENADOR", "ADMIN"}:
            raise ValidationError({
                "creado_por": "Los ejercicios personalizados deben ser registrados por un entrenador."
            })

    def __str__(self):
        return self.nombre


class EjercicioEquipamiento(models.Model):
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name="equipamientos_asociados",
    )
    equipamiento = models.ForeignKey(
        Equipamiento,
        on_delete=models.PROTECT,
        related_name="ejercicios_asociados",
    )

    class Meta:
        ordering = ("ejercicio", "equipamiento")
        constraints = [
            models.UniqueConstraint(
                fields=("ejercicio", "equipamiento"),
                name="ejercicio_equipo_unico",
            ),
        ]

    def __str__(self):
        return f"{self.ejercicio} - {self.equipamiento}"


class Rutina(models.Model):
    NIVELES = [
        ("BASICO", "Básico"),
        ("INTERMEDIO", "Intermedio"),
        ("AVANZADO", "Avanzado"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutinas",
    )
    creador = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutinas_creadas",
    )
    objetivo = models.ForeignKey(
        "clientes.Objetivo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutinas",
    )
    nivel = models.CharField(max_length=20, choices=NIVELES, default="BASICO")
    duracion_semanas = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    es_predefinida = models.BooleanField(default=False)
    es_publica = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("nombre",)
        constraints = [
            models.CheckConstraint(
                condition=Q(duracion_semanas__gte=1),
                name="rutina_duracion_gte_1",
            ),
        ]

    def clean(self):
        if self.creador_id and self.creador.rol not in {"ENTRENADOR", "ADMIN"}:
            raise ValidationError({
                "creador": "Las rutinas oficiales deben ser creadas por un entrenador."
            })

    def __str__(self):
        return self.nombre


class RutinaDia(models.Model):
    DIAS_SEMANA = [
        ("LUNES", "Lunes"),
        ("MARTES", "Martes"),
        ("MIERCOLES", "Miércoles"),
        ("JUEVES", "Jueves"),
        ("VIERNES", "Viernes"),
        ("SABADO", "Sábado"),
        ("DOMINGO", "Domingo"),
    ]

    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name="dias",
    )
    dia_semana = models.CharField(
        max_length=12,
        choices=DIAS_SEMANA,
        null=True,
        blank=True,
    )
    nombre = models.CharField(max_length=80, default="Día de entrenamiento")
    orden = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ("rutina", "orden")
        constraints = [
            models.UniqueConstraint(
                fields=("rutina", "orden"),
                name="rutina_dia_orden_unico",
            ),
            models.UniqueConstraint(
                fields=("rutina", "dia_semana"),
                condition=Q(dia_semana__isnull=False),
                name="rutina_dia_semana_unico",
            ),
            models.CheckConstraint(
                condition=Q(orden__gte=1),
                name="rutina_dia_orden_positivo",
            ),
        ]

    def __str__(self):
        return f"{self.rutina} - {self.nombre}"


class RutinaEjercicio(models.Model):
    rutina_dia = models.ForeignKey(
        RutinaDia,
        on_delete=models.CASCADE,
        related_name="ejercicios",
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.PROTECT,
        related_name="rutinas",
    )
    orden = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    series = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1)],
    )
    repeticiones = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
    )
    peso_objetivo = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    descanso_segundos = models.PositiveIntegerField(default=60)
    duracion_segundos = models.PositiveIntegerField(null=True, blank=True)
    intensidad = models.CharField(max_length=50, blank=True)
    observaciones = models.TextField(blank=True)

    @property
    def rutina(self):
        return self.rutina_dia.rutina

    class Meta:
        ordering = ("rutina_dia", "orden")
        constraints = [
            models.UniqueConstraint(
                fields=("rutina_dia", "ejercicio"),
                name="rut_dia_ejercicio_unico",
            ),
            models.UniqueConstraint(
                fields=("rutina_dia", "orden"),
                name="rut_dia_ejercicio_orden",
            ),
            models.CheckConstraint(
                condition=Q(orden__gte=1, series__gte=1, repeticiones__gte=1),
                name="rut_ejercicio_valores_positivos",
            ),
            models.CheckConstraint(
                condition=Q(peso_objetivo__isnull=True) | Q(peso_objetivo__gt=0),
                name="rut_ejercicio_peso_positivo",
            ),
        ]

    def __str__(self):
        return f"{self.rutina_dia} - {self.ejercicio}"


class AsignacionRutina(models.Model):
    ESTADOS = [
        ("ACTIVA", "Activa"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ]

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        related_name="rutinas_asignadas",
    )
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.PROTECT,
        related_name="asignaciones",
    )
    asignada_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asignaciones_rutina_realizadas",
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="ACTIVA")
    observaciones = models.TextField(blank=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-fecha_inicio",)
        constraints = [
            models.CheckConstraint(
                condition=Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F("fecha_inicio")),
                name="asig_rutina_fechas_validas",
            ),
            models.UniqueConstraint(
                fields=("cliente",),
                condition=Q(estado="ACTIVA"),
                name="cliente_una_rutina_activa",
            ),
        ]

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({
                "fecha_fin": "La fecha final no puede ser anterior a la fecha inicial."
            })
        if self.asignada_por_id and self.asignada_por.rol not in {"ENTRENADOR", "ADMIN"}:
            raise ValidationError({
                "asignada_por": "Solo un entrenador puede asignar oficialmente una rutina."
            })
        if self.estado == "ACTIVA":
            activas = type(self).objects.filter(cliente_id=self.cliente_id, estado="ACTIVA")
            if self.pk:
                activas = activas.exclude(pk=self.pk)
            if activas.exists():
                raise ValidationError({
                    "estado": "El cliente ya tiene una rutina activa."
                })

    def __str__(self):
        return f"{self.cliente} - {self.rutina}"


class SesionEntrenamiento(models.Model):
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        related_name="sesiones_entrenamiento",
    )
    asignacion_rutina = models.ForeignKey(
        AsignacionRutina,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sesiones",
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    duracion_minutos = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ("-fecha", "-hora_inicio")
        constraints = [
            models.CheckConstraint(
                condition=Q(hora_inicio__isnull=True)
                | Q(hora_fin__isnull=True)
                | Q(hora_fin__gte=F("hora_inicio")),
                name="sesion_horas_validas",
            ),
        ]

    def clean(self):
        if (
            self.asignacion_rutina_id
            and self.cliente_id
            and self.asignacion_rutina.cliente_id != self.cliente_id
        ):
            raise ValidationError({
                "asignacion_rutina": "La rutina asignada debe pertenecer al cliente de la sesión."
            })

    def save(self, *args, **kwargs):
        if self.hora_inicio and self.hora_fin:
            inicio = self.hora_inicio.hour * 60 + self.hora_inicio.minute
            fin = self.hora_fin.hour * 60 + self.hora_fin.minute
            self.duracion_minutos = fin - inicio
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = tuple(
                    dict.fromkeys((*kwargs["update_fields"], "duracion_minutos"))
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sesión de {self.cliente} - {self.fecha}"


class EjercicioRealizado(models.Model):
    sesion = models.ForeignKey(
        SesionEntrenamiento,
        on_delete=models.CASCADE,
        related_name="ejercicios_realizados",
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.PROTECT,
        related_name="registros_realizados",
    )
    dificultad_percibida = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    orden = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ("sesion", "orden")
        constraints = [
            models.UniqueConstraint(
                fields=("sesion", "orden"),
                name="sesion_ejercicio_orden_unico",
            ),
            models.CheckConstraint(
                condition=Q(dificultad_percibida__isnull=True)
                | Q(dificultad_percibida__gte=1, dificultad_percibida__lte=10),
                name="dificultad_percibida_rango",
            ),
        ]

    def __str__(self):
        return f"{self.sesion} - {self.ejercicio}"


class SerieRealizada(models.Model):
    ejercicio_realizado = models.ForeignKey(
        EjercicioRealizado,
        on_delete=models.CASCADE,
        related_name="series",
    )
    numero_serie = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    repeticiones = models.PositiveIntegerField()
    peso_utilizado = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    duracion_segundos = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ("ejercicio_realizado", "numero_serie")
        constraints = [
            models.UniqueConstraint(
                fields=("ejercicio_realizado", "numero_serie"),
                name="ejercicio_serie_numero_unico",
            ),
            models.CheckConstraint(
                condition=Q(numero_serie__gte=1),
                name="numero_serie_positivo",
            ),
        ]

    def __str__(self):
        return f"Serie {self.numero_serie} - {self.ejercicio_realizado}"
