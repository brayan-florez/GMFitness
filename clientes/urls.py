from django.urls import path
from . import views

urlpatterns = [
    # CRUD de objetivos
    path('objetivos/', views.listar_objetivos, name='listar_objetivos'),
    path('objetivos/crear/', views.crear_objetivo, name='crear_objetivo'),
    path('objetivos/editar/<int:id>/', views.editar_objetivo, name='editar_objetivo'),
    path('objetivos/eliminar/<int:id>/', views.eliminar_objetivo, name='eliminar_objetivo'),
]
