from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Usuario(models.Model):

    USERNAME_FIELD = "correo"

    ROLES = [
        ("ADMIN", "Administrador"),
        ("CLIENTE", "Cliente"),
        ("ENTRENADOR", "Entrenador"),
        ("NUTRICIONISTA", "Nutricionista"),
        ("FISIOTERAPEUTA", "Fisioterapeuta"),
    ]

    SEXOS = [
        ("HOMBRE", "Hombre"),
        ("MUJER", "Mujer"),
        ("OTRO", "Otro"),
    ]

    nombre = models.CharField(max_length=100)

    apellido = models.CharField(max_length=100)

    documento = models.CharField(
        max_length=20,
        unique=True
    )

    fecha_nacimiento = models.DateField()

    sexo = models.CharField(
        max_length=20,
        choices=SEXOS
    )

    telefono = models.CharField(
        max_length=20
    )

    correo = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    foto = models.ImageField(
        upload_to="usuarios/",
        blank=True,
        null=True
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES
    )

    sede = models.ForeignKey(
        "gimnasios.Sede",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios"
    )

    activo = models.BooleanField(
        default=True
    )

    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Última sesión"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def establecer_password(self, password):
        self.password = make_password(password)

    def verificar_password(self, password):
        return check_password(password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.activo

    def get_username(self):
        return self.correo

    def get_session_auth_hash(self):
        return self.password

    def tiene_rol(self, *roles):
        return self.rol in roles

    def __str__(self):
        return f"{self.nombre} {self.apellido}"