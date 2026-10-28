from django.urls import path
from common.crud import crud_patterns

from .forms import ClienteProfileForm, MedicionFisicaForm
from .models import Cliente, MedicionFisica
from . import views

urlpatterns = [
    # CRUD de objetivos
    path('objetivos/', views.listar_objetivos, name='listar_objetivos'),
    path('objetivos/crear/', views.crear_objetivo, name='crear_objetivo'),
    path('objetivos/editar/<int:id>/', views.editar_objetivo, name='editar_objetivo'),
    path('objetivos/eliminar/<int:id>/', views.eliminar_objetivo, name='eliminar_objetivo'),
]

urlpatterns += crud_patterns(
    Cliente,
    "clientes",
    "Clientes",
    route="clientes",
    search_fields=("usuario__nombre", "usuario__apellido", "usuario__documento"),
    display_fields=("usuario", "usuario__correo", "objetivo", "activo"),
    form_class=ClienteProfileForm,
    soft_delete_field="activo",
)

urlpatterns += crud_patterns(
    MedicionFisica,
    "mediciones_fisicas",
    "Mediciones físicas",
    route="mediciones-fisicas",
    search_fields=("cliente__usuario__nombre", "cliente__usuario__apellido"),
    display_fields=("cliente", "fecha_medicion", "peso", "altura", "imc", "porcentaje_grasa"),
    form_class=MedicionFisicaForm,
)
