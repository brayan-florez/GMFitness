from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone


class Pago(models.Model):
    METODOS = [
        ("TARJETA", "Tarjeta"),
        ("PSE", "PSE"),
        ("TRANSFERENCIA", "Transferencia"),
        ("EFECTIVO", "Efectivo"),
    ]
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("APROBADO", "Aprobado"),
        ("RECHAZADO", "Rechazado"),
        ("REEMBOLSADO", "Reembolsado"),
    ]

    membresia = models.ForeignKey(
        "membresias.Membresia",
        on_delete=models.PROTECT,
        related_name="pagos",
    )
    fecha_pago = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="PENDIENTE")
    referencia = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ("-fecha_pago",)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name="pago_monto_positivo",
            ),
        ]

    def __str__(self):
        return f"Pago {self.pk or 'nuevo'} - {self.monto}"

    @transaction.atomic
    def aprobar(self):
        """Confirma un pago simulado, activa la membresía y emite su recibo."""
        pago = type(self).objects.select_for_update().select_related(
            "membresia"
        ).get(pk=self.pk)
        if pago.estado == "APROBADO":
            return getattr(pago, "factura", None)
        if pago.estado != "PENDIENTE":
            raise ValidationError("Solo se pueden aprobar pagos pendientes.")
        if pago.membresia.estado == "CANCELADA":
            raise ValidationError("No se puede aprobar el pago de una membresía cancelada.")
        if pago.monto != pago.membresia.precio_pagado:
            raise ValidationError("El pago debe coincidir con el precio registrado en la membresía.")

        pago.estado = "APROBADO"
        pago.save(update_fields=("estado",))

        membresia = pago.membresia
        membresia.estado = "ACTIVA"
        membresia.save(update_fields=("estado",))

        factura, _ = Factura.objects.get_or_create(
            pago=pago,
            defaults={
                "subtotal": pago.monto,
                "total": pago.monto,
                "detalle": f"Pago de membresía {membresia.plan_precio.plan.nombre}",
            },
        )
        return factura


class Factura(models.Model):
    pago = models.OneToOneField(
        Pago,
        on_delete=models.PROTECT,
        related_name="factura",
    )
    numero = models.CharField(max_length=32, unique=True, blank=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    detalle = models.TextField(blank=True)

    class Meta:
        ordering = ("-fecha_emision",)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0, subtotal__gte=0),
                name="factura_totales_no_negativos",
            ),
        ]

    def clean(self):
        if self.pago_id and self.pago.estado != "APROBADO":
            raise ValidationError({
                "pago": "El recibo solo se emite para pagos aprobados."
            })
        if self.pago_id and self.total is not None and self.total != self.pago.monto:
            raise ValidationError({
                "total": "El total del recibo debe coincidir con el pago registrado."
            })

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f"GMF-{timezone.localdate():%Y%m%d}-{uuid4().hex[:10].upper()}"
        if self.pago_id:
            if self.subtotal is None:
                self.subtotal = self.pago.monto
            if self.total is None:
                self.total = self.pago.monto
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero or "Factura pendiente"
