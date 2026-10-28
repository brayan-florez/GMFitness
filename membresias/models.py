from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class PlanMembresia(models.Model):
    NIVELES = [
        ("BASICO", "Básico"),
        ("PREMIUM", "Premium"),
        ("BLACK", "Black"),
    ]

    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.CASCADE,
        related_name="planes_membresia",
    )
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=12, choices=NIVELES)
    beneficios = models.ManyToManyField(
        "Beneficio",
        through="PlanBeneficio",
        related_name="planes",
        blank=True,
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ("sede", "nivel", "nombre")
        constraints = [
            models.UniqueConstraint(
                fields=("sede", "nivel"),
                name="plan_nivel_unico_por_sede",
            ),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.sede})"


class Beneficio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ("nombre",)

    def __str__(self):
        return self.nombre


class PlanBeneficio(models.Model):
    plan = models.ForeignKey(
        PlanMembresia,
        on_delete=models.CASCADE,
        related_name="beneficios_asignados",
    )
    beneficio = models.ForeignKey(
        Beneficio,
        on_delete=models.PROTECT,
        related_name="planes_asignados",
    )
    detalle = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("plan", "beneficio"),
                name="beneficio_unico_por_plan",
            ),
        ]

    def __str__(self):
        return f"{self.plan} - {self.beneficio}"


class PlanPrecio(models.Model):
    PERIODICIDADES = [
        ("MENSUAL", "Mensual"),
        ("TRIMESTRAL", "Trimestral"),
        ("ANUAL", "Anual"),
    ]

    plan = models.ForeignKey(
        PlanMembresia,
        on_delete=models.CASCADE,
        related_name="precios",
    )
    periodicidad = models.CharField(max_length=12, choices=PERIODICIDADES)
    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    duracion_dias = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("plan", "periodicidad", "-fecha_creacion")
        constraints = [
            models.UniqueConstraint(
                fields=("plan", "periodicidad"),
                condition=Q(activo=True),
                name="plan_precio_activo_unico",
            ),
            models.CheckConstraint(
                condition=Q(precio__gt=0, duracion_dias__gte=1),
                name="plan_precio_valido",
            ),
        ]

    def __str__(self):
        return f"{self.plan} - {self.get_periodicidad_display()}"


class Membresia(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente de pago"),
        ("ACTIVA", "Activa"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ]

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="membresias",
    )
    plan_precio = models.ForeignKey(
        PlanPrecio,
        on_delete=models.PROTECT,
        related_name="membresias",
    )
    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.PROTECT,
        related_name="membresias",
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="PENDIENTE")
    precio_pagado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-fecha_inicio",)
        constraints = [
            models.CheckConstraint(
                condition=Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F("fecha_inicio")),
                name="membresia_fechas_validas",
            ),
            models.CheckConstraint(
                condition=Q(precio_pagado__gt=0),
                name="membresia_precio_positivo",
            ),
        ]

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({
                "fecha_fin": "La fecha final no puede ser anterior a la fecha inicial."
            })
        if self.plan_precio_id and self.sede_id:
            if self.plan_precio.plan.sede_id != self.sede_id:
                raise ValidationError({
                    "sede": "La sede debe coincidir con la sede del plan seleccionado."
                })

    def save(self, *args, **kwargs):
        if self.plan_precio_id and self.precio_pagado is None:
            self.precio_pagado = self.plan_precio.precio
        if self.plan_precio_id and self.fecha_inicio and self.fecha_fin is None:
            from datetime import timedelta

            self.fecha_fin = self.fecha_inicio + timedelta(
                days=self.plan_precio.duracion_dias - 1
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.plan_precio.plan} ({self.estado})"
