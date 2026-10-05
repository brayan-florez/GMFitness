from django.db import models


class Dieta(models.Model):

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
        related_name="dietas"
    )

    creador = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dietas_creadas"
    )

    activa = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre


class ComidaDieta(models.Model):

    dieta = models.ForeignKey(
        Dieta,
        on_delete=models.CASCADE,
        related_name="comidas"
    )

    nombre = models.CharField(
        max_length=100
    )

    orden = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.dieta} - {self.nombre}"


class Alimento(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nombre


class ComidaAlimento(models.Model):

    comida = models.ForeignKey(
        ComidaDieta,
        on_delete=models.CASCADE,
        related_name="alimentos"
    )

    alimento = models.ForeignKey(
        Alimento,
        on_delete=models.CASCADE,
        related_name="comidas"
    )

    cantidad = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    unidad = models.CharField(
        max_length=30
    )

    def __str__(self):
        return f"{self.comida} - {self.alimento}"


class AsignacionDieta(models.Model):

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        related_name="dietas_asignadas"
    )

    dieta = models.ForeignKey(
        Dieta,
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

    activa = models.BooleanField(
        default=True
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.cliente} - {self.dieta}"