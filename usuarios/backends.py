from django.contrib.auth.backends import BaseBackend

from .models import Usuario


class EmailBackend(BaseBackend):
    """Autenticación usando correo y contraseña del modelo Usuario."""

    def authenticate(self, request, correo=None, password=None, **kwargs):
        if not correo or not password:
            return None

        try:
            usuario = Usuario.objects.get(correo__iexact=correo, activo=True)
        except Usuario.DoesNotExist:
            return None

        if usuario.verificar_password(password):
            return usuario

        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id, activo=True)
        except Usuario.DoesNotExist:
            return None
