from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Gestión de usuarios
    path('', include('usuarios.urls')),

    # Gestión de perfiles profesionales
    path('', include('profesionales.urls')),

    # Gestión de membresías
    path('', include('membresias.urls')),

    # Pagos, facturas y citas
    path('', include('pagos.urls')),
    path('', include('citas.urls')),

    # Página de inicio y gestión de sedes
    path('', include('gimnasios.urls')),

    # Módulo de clientes: gestión de objetivos
    path('', include('clientes.urls')),

    # Módulo de entrenamientos: gestión de ejercicios
    path('', include('entrenamientos.urls')),

    # Módulo de nutrición: gestión de alimentos
    path('', include('nutricion.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
