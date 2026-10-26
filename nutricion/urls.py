from django.urls import path
from . import views

urlpatterns = [
    # CRUD de alimentos
    path('alimentos/', views.listar_alimentos, name='listar_alimentos'),
    path('alimentos/crear/', views.crear_alimento, name='crear_alimento'),
    path('alimentos/editar/<int:id>/', views.editar_alimento, name='editar_alimento'),
    path('alimentos/eliminar/<int:id>/', views.eliminar_alimento, name='eliminar_alimento'),
]
