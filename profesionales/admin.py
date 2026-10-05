from django.contrib import admin

from .models import Entrenador, Nutricionista, Fisioterapeuta


admin.site.register(Entrenador)
admin.site.register(Nutricionista)
admin.site.register(Fisioterapeuta)