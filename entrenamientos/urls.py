from django.urls import path
from . import views

urlpatterns = [
    # CRUD de ejercicios
    path('ejercicios/', views.listar_ejercicios, name='listar_ejercicios'),
    path('ejercicios/crear/', views.crear_ejercicio, name='crear_ejercicio'),
    path('ejercicios/editar/<int:id>/', views.editar_ejercicio, name='editar_ejercicio'),
    path('ejercicios/eliminar/<int:id>/', views.eliminar_ejercicio, name='eliminar_ejercicio'),
]
