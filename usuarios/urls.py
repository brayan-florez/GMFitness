from common.crud import crud_patterns
from .forms import UsuarioChangeForm, UsuarioCreationForm
from .models import Usuario


urlpatterns = crud_patterns(
    Usuario,
    "usuarios",
    "Usuarios",
    route="usuarios",
    search_fields=("nombre", "apellido", "correo", "documento"),
    display_fields=("nombre", "apellido", "correo", "rol_display", "activo"),
    form_class=(UsuarioCreationForm, UsuarioChangeForm),
    soft_delete_field="activo",
)
