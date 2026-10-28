from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Q
from django.utils import timezone


class DisponibilidadFisioterapeuta(models.Model):
    ESTADOS = [
        ("DISPONIBLE", "Disponible"),
        ("RESERVADA", "Reservada"),
        ("BLOQUEADA", "Bloqueada"),
    ]

    fisioterapeuta = models.ForeignKey(
        "profesionales.Fisioterapeuta",
        on_delete=models.PROTECT,
        related_name="disponibilidades",
    )
    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.PROTECT,
        related_name="disponibilidades_fisioterapia",
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default="DISPONIBLE")

    class Meta:
        ordering = ("fecha", "hora_inicio")
        constraints = [
            models.CheckConstraint(
                condition=Q(hora_fin__gt=F("hora_inicio")),
                name="disponibilidad_hora_fin_posterior",
            ),
            models.UniqueConstraint(
                fields=("fisioterapeuta", "fecha", "hora_inicio"),
                name="fisio_hora_inicio_unica",
            ),
        ]

    def clean(self):
        if self.hora_inicio and self.hora_fin and self.hora_fin <= self.hora_inicio:
            raise ValidationError({
                "hora_fin": "La hora de finalización debe ser posterior al inicio."
            })
        if (
            self.fisioterapeuta_id
            and self.sede_id
            and self.fisioterapeuta.usuario.sede_id
            and self.fisioterapeuta.usuario.sede_id != self.sede_id
        ):
            raise ValidationError({
                "sede": "La cita debe programarse en la sede del fisioterapeuta."
            })
        if not all((self.fisioterapeuta_id, self.fecha, self.hora_inicio, self.hora_fin)):
            return
        solapadas = type(self).objects.filter(
            fisioterapeuta=self.fisioterapeuta,
            fecha=self.fecha,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio,
        )
        if self.pk:
            solapadas = solapadas.exclude(pk=self.pk)
        if solapadas.exists():
            raise ValidationError("El horario se cruza con otra disponibilidad del fisioterapeuta.")

    def __str__(self):
        return f"{self.fisioterapeuta} - {self.fecha} {self.hora_inicio:%H:%M}"


class Cita(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("RECHAZADA", "Rechazada"),
        ("CANCELADA", "Cancelada"),
        ("COMPLETADA", "Completada"),
    ]

    disponibilidad = models.ForeignKey(
        DisponibilidadFisioterapeuta,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="citas_fisioterapia",
    )
    fecha_reserva = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="PENDIENTE")
    motivo = models.CharField(max_length=250, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ("-fecha_reserva",)
        constraints = [
            models.UniqueConstraint(
                fields=("disponibilidad",),
                condition=Q(estado__in=("PENDIENTE", "CONFIRMADA")),
                name="disponibilidad_una_cita_activa",
            ),
        ]

    def clean(self):
        if self.cliente_id and self.cliente.usuario.rol != "CLIENTE":
            raise ValidationError({
                "cliente": "La cita debe quedar asociada a un cliente."
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        previous_availability_id = None
        if self.pk:
            previous = type(self).objects.select_for_update().filter(pk=self.pk).first()
            if previous:
                previous_availability_id = previous.disponibilidad_id

        disponibilidad = DisponibilidadFisioterapeuta.objects.select_for_update().get(
            pk=self.disponibilidad_id
        )

        if not self.pk or previous_availability_id != self.disponibilidad_id:
            if disponibilidad.estado != "DISPONIBLE":
                raise ValidationError("El horario seleccionado ya no está disponible.")

        super().save(*args, **kwargs)

        if self.estado in {"CANCELADA", "RECHAZADA"}:
            disponibilidad.estado = "DISPONIBLE"
        else:
            disponibilidad.estado = "RESERVADA"
        disponibilidad.save(update_fields=("estado",))

        if previous_availability_id and previous_availability_id != self.disponibilidad_id:
            DisponibilidadFisioterapeuta.objects.filter(
                pk=previous_availability_id
            ).update(estado="DISPONIBLE")

    def delete(self, *args, **kwargs):
        disponibilidad = self.disponibilidad
        with transaction.atomic():
            result = super().delete(*args, **kwargs)
            disponibilidad.estado = "DISPONIBLE"
            disponibilidad.save(update_fields=("estado",))
        return result

    def __str__(self):
        return f"Cita de {self.cliente} - {self.disponibilidad.fecha}"
