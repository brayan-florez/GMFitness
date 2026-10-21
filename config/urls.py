from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Módulo de gimnasios: gestión de sedes
    path('', include('gimnasios.urls')),
]