from django.db import models
from usuarios.models import Usuario


class Entrenador(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_entrenador"
    )

    especialidad = models.CharField(
        max_length=100,
        blank=True
    )

    experiencia = models.PositiveIntegerField(
        default=0
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"


class Nutricionista(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_nutricionista"
    )

    especialidad = models.CharField(
        max_length=100,
        blank=True
    )

    registro_profesional = models.CharField(
        max_length=50,
        blank=True
    )

    experiencia = models.PositiveIntegerField(
        default=0
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"


class Fisioterapeuta(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_fisioterapeuta"
    )

    especialidad = models.CharField(
        max_length=100,
        blank=True
    )

    registro_profesional = models.CharField(
        max_length=50,
        blank=True
    )

    experiencia = models.PositiveIntegerField(
        default=0
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"