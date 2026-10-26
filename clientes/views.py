from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ObjetivoForm
from .models import Objetivo


# Listar todos los objetivos
def listar_objetivos(request):
    objetivos = Objetivo.objects.all().order_by("nombre")

    contexto = {
        "objetivos": objetivos
    }

    return render(request, "objetivos/listar_objetivos.html", contexto)


# Registrar un objetivo
def crear_objetivo(request):
    if request.method == "POST":
        form = ObjetivoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "El objetivo se registró correctamente.")
            return redirect("listar_objetivos")

    else:
        form = ObjetivoForm()

    contexto = {
        "form": form,
        "titulo": "Registrar objetivo",
        "boton": "Guardar"
    }

    return render(request, "objetivos/formulario_objetivo.html", contexto)


# Editar un objetivo
def editar_objetivo(request, id):
    objetivo = get_object_or_404(Objetivo, pk=id)

    if request.method == "POST":
        form = ObjetivoForm(request.POST, instance=objetivo)

        if form.is_valid():
            form.save()
            messages.success(request, "El objetivo se actualizó correctamente.")
            return redirect("listar_objetivos")

    else:
        form = ObjetivoForm(instance=objetivo)

    contexto = {
        "form": form,
        "titulo": "Editar objetivo",
        "boton": "Actualizar",
        "objetivo": objetivo
    }

    return render(request, "objetivos/formulario_objetivo.html", contexto)


# Eliminar un objetivo con confirmación
def eliminar_objetivo(request, id):
    objetivo = get_object_or_404(Objetivo, pk=id)

    if request.method == "POST":
        nombre = objetivo.nombre

        try:
            objetivo.delete()
        except IntegrityError:
            messages.error(
                request,
                "No se pudo eliminar el objetivo porque está relacionado "
                "con otros registros."
            )
            return redirect("listar_objetivos")

        messages.success(
            request,
            f"El objetivo '{nombre}' se eliminó correctamente."
        )
        return redirect("listar_objetivos")

    return render(
        request,
        "objetivos/eliminar_objetivo.html",
        {"objetivo": objetivo}
    )
