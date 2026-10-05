from django.db import models


class Ejercicio(models.Model):

    DIFICULTADES = [
        ("BASICO", "Básico"),
        ("INTERMEDIO", "Intermedio"),
        ("AVANZADO", "Avanzado"),
    ]

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    grupo_muscular = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True
    )

    instrucciones = models.TextField(
        blank=True
    )

    equipo = models.CharField(
        max_length=100,
        blank=True
    )

    dificultad = models.CharField(
        max_length=20,
        choices=DIFICULTADES,
        default="BASICO"
    )

    imagen = models.ImageField(
        upload_to="ejercicios/",
        blank=True,
        null=True
    )

    video = models.URLField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre


class Rutina(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True
    )

    objetivo = models.ForeignKey(
        "clientes.Objetivo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutinas"
    )

    creador = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutinas_creadas"
    )

    es_predefinida = models.BooleanField(
        default=False
    )

    duracion_semanas = models.PositiveIntegerField(
        default=1
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre


class RutinaEjercicio(models.Model):

    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name="ejercicios"
    )

    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name="rutinas"
    )

    orden = models.PositiveIntegerField(
        default=1
    )

    series = models.PositiveIntegerField(
        default=3
    )

    repeticiones = models.PositiveIntegerField(
        default=10
    )

    peso = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    descanso_segundos = models.PositiveIntegerField(
        default=60
    )

    intensidad = models.CharField(
        max_length=50,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.rutina} - {self.ejercicio}"


class AsignacionRutina(models.Model):

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        related_name="rutinas_asignadas"
    )

    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name="asignaciones"
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.cliente} - {self.rutina}"