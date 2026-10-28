from common.crud import crud_patterns

from .forms import (
    EntrenadorProfileForm,
    FisioterapeutaProfileForm,
    NutricionistaProfileForm,
)
from .models import Entrenador, Fisioterapeuta, Nutricionista


urlpatterns = []

urlpatterns += crud_patterns(
    Entrenador,
    "entrenadores",
    "Entrenadores",
    route="entrenadores",
    search_fields=("usuario__nombre", "usuario__apellido", "usuario__documento"),
    display_fields=("usuario", "especialidad", "experiencia", "activo"),
    form_class=EntrenadorProfileForm,
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    Nutricionista,
    "nutricionistas",
    "Nutricionistas",
    route="nutricionistas",
    search_fields=("usuario__nombre", "usuario__apellido", "usuario__documento"),
    display_fields=("usuario", "especialidad", "registro_profesional", "activo"),
    form_class=NutricionistaProfileForm,
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    Fisioterapeuta,
    "fisioterapeutas",
    "Fisioterapeutas",
    route="fisioterapeutas",
    search_fields=("usuario__nombre", "usuario__apellido", "usuario__documento"),
    display_fields=("usuario", "especialidad", "registro_profesional", "activo"),
    form_class=FisioterapeutaProfileForm,
    soft_delete_field="activo",
)
