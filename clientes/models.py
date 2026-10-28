from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
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
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    altura = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
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
        blank=True,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ],
    )

    cintura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    cadera = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    pecho = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    brazo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    muslo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    observaciones = models.TextField(
        blank=True
    )

    fecha_medicion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ("-fecha_medicion",)
        constraints = [
            models.CheckConstraint(
                condition=Q(peso__gt=0),
                name="medicion_peso_mayor_cero",
            ),
            models.CheckConstraint(
                condition=Q(altura__gt=0),
                name="medicion_altura_mayor_cero",
            ),
            models.CheckConstraint(
                condition=Q(porcentaje_grasa__isnull=True)
                | Q(porcentaje_grasa__gte=0, porcentaje_grasa__lte=100),
                name="medicion_grasa_rango_valido",
            ),
            models.CheckConstraint(
                condition=Q(cintura__isnull=True) | Q(cintura__gt=0),
                name="medicion_cintura_positiva",
            ),
            models.CheckConstraint(
                condition=Q(cadera__isnull=True) | Q(cadera__gt=0),
                name="medicion_cadera_positiva",
            ),
            models.CheckConstraint(
                condition=Q(pecho__isnull=True) | Q(pecho__gt=0),
                name="medicion_pecho_positivo",
            ),
            models.CheckConstraint(
                condition=Q(brazo__isnull=True) | Q(brazo__gt=0),
                name="medicion_brazo_positivo",
            ),
            models.CheckConstraint(
                condition=Q(muslo__isnull=True) | Q(muslo__gt=0),
                name="medicion_muslo_positivo",
            ),
        ]

    def save(self, *args, **kwargs):
        # La estatura se almacena en metros y el peso en kilogramos.
        if self.peso is not None and self.altura is not None and self.altura > 0:
            self.imc = (self.peso / (self.altura ** 2)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = tuple(
                    dict.fromkeys((*kwargs["update_fields"], "imc"))
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Medición de {self.cliente} - {self.fecha_medicion:%Y-%m-%d}"
