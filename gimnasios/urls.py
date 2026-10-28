from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    # CRUD de sedes
    path('sedes/', views.listar_sedes, name='listar_sedes'),
    path('sedes/crear/', views.crear_sede, name='crear_sede'),
    path('sedes/editar/<int:id>/', views.editar_sede, name='editar_sede'),
    path('sedes/eliminar/<int:id>/', views.eliminar_sede, name='eliminar_sede'),
]
