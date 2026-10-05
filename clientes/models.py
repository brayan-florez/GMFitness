from django.db import models
from usuarios.models import Usuario


class Objetivo(models.Model):

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


class Cliente(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_cliente"
    )

    objetivo = models.ForeignKey(
        Objetivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"


class MedicionFisica(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="mediciones"
    )

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    altura = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    imc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    porcentaje_grasa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    cintura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    cadera = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    pecho = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    fecha_medicion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Medición de {self.cliente} - {self.fecha_medicion:%Y-%m-%d}"