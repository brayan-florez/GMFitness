from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class Dieta(models.Model):

    creador = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dietas_creadas",
    )

    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dietas",
    )

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

    calorias_objetivo = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )

    es_publica = models.BooleanField(default=True)

    activa = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if self.creador_id and self.creador.rol not in {"NUTRICIONISTA", "ADMIN"}:
            raise ValidationError({
                "creador": "Las dietas oficiales deben ser creadas por un nutricionista."
            })

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ("nombre",)


class ComidaDieta(models.Model):

    TIPOS_COMIDA = [
        ("DESAYUNO", "Desayuno"),
        ("MEDIA_MANANA", "Media mañana"),
        ("ALMUERZO", "Almuerzo"),
        ("MEDIA_TARDE", "Media tarde"),
        ("CENA", "Cena"),
        ("SNACK", "Snack"),
        ("OTRO", "Otro"),
    ]

    dieta = models.ForeignKey(
        Dieta,
        on_delete=models.CASCADE,
        related_name="comidas"
    )

    nombre = models.CharField(
        max_length=100
    )

    tipo_comida = models.CharField(
        max_length=20,
        choices=TIPOS_COMIDA,
        default="OTRO",
    )

    hora_recomendada = models.TimeField(null=True, blank=True)

    orden = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        return f"{self.dieta} - {self.nombre}"

    class Meta:
        ordering = ("dieta", "orden")
        constraints = [
            models.UniqueConstraint(
                fields=("dieta", "orden"),
                name="comida_dieta_orden_unico",
            ),
            models.CheckConstraint(
                condition=Q(orden__gte=1),
                name="comida_dieta_orden_positivo",
            ),
        ]


class Alimento(models.Model):

    creado_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alimentos_creados",
    )

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    codigo_barras = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    descripcion = models.TextField(
        blank=True
    )

    porcion_referencia = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal("100.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    unidad_porcion = models.CharField(max_length=30, default="g")

    calorias = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    proteinas = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    carbohidratos = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    grasas = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    fibra = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    imagen = models.ImageField(upload_to="alimentos/", null=True, blank=True)

    activo = models.BooleanField(
        default=True
    )

    def clean(self):
        if self.creado_por_id and self.creado_por.rol not in {"CLIENTE", "NUTRICIONISTA", "ADMIN"}:
            raise ValidationError({
                "creado_por": "Solo un cliente o nutricionista puede registrar alimentos."
            })

    class Meta:
        ordering = ("nombre",)
        constraints = [
            models.CheckConstraint(
                condition=Q(porcion_referencia__gt=0),
                name="porcion_alimento_positiva",
            ),
            models.CheckConstraint(
                condition=Q(calorias__gte=0, proteinas__gte=0, carbohidratos__gte=0,
                            grasas__gte=0, fibra__gte=0),
                name="nutrientes_no_negativos",
            ),
        ]

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
        on_delete=models.PROTECT,
        related_name="comidas"
    )

    cantidad = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    unidad = models.CharField(
        max_length=30
    )

    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.comida} - {self.alimento}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("comida", "alimento"),
                name="alimento_unico_por_comida",
            ),
            models.CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="cantidad_alimento_mayor_cero",
            ),
        ]


class AsignacionDieta(models.Model):

    ESTADOS = [
        ("ACTIVA", "Activa"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ]

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

    asignada_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dietas_asignadas",
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    estado = models.CharField(max_length=12, choices=ESTADOS, default="ACTIVA")

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({
                "fecha_fin": "La fecha final no puede ser anterior a la fecha inicial."
            })
        if self.asignada_por_id and self.asignada_por.rol not in {"NUTRICIONISTA", "ADMIN"}:
            raise ValidationError({
                "asignada_por": "Solo un nutricionista puede asignar oficialmente una dieta."
            })

    def __str__(self):
        return f"{self.cliente} - {self.dieta}"

    class Meta:
        ordering = ("-fecha_inicio",)
        constraints = [
            models.CheckConstraint(
                condition=Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F("fecha_inicio")),
                name="asig_dieta_fechas_validas",
            ),
        ]
