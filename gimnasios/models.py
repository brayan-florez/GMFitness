from django.db import models


class Sede(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    direccion = models.CharField(
        max_length=200
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre