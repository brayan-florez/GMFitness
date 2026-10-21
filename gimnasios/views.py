from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Sede
from .forms import SedeForm


# Listar todas las sedes
def listar_sedes(request):
    sedes = Sede.objects.all().order_by("nombre")

    contexto = {
        "sedes": sedes
    }

    return render(request, "sedes/listar_sedes.html", contexto)


# Registrar una sede
def crear_sede(request):
    if request.method == "POST":
        form = SedeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "La sede se registró correctamente.")
            return redirect("listar_sedes")

    else:
        form = SedeForm()

    contexto = {
        "form": form,
        "titulo": "Registrar sede",
        "boton": "Guardar"
    }

    return render(request, "sedes/formulario_sede.html", contexto)


# Editar una sede
def editar_sede(request, id):
    sede = get_object_or_404(Sede, pk=id)

    if request.method == "POST":
        form = SedeForm(request.POST, instance=sede)

        if form.is_valid():
            form.save()
            messages.success(request, "La sede se actualizó correctamente.")
            return redirect("listar_sedes")

    else:
        form = SedeForm(instance=sede)

    contexto = {
        "form": form,
        "titulo": "Editar sede",
        "boton": "Actualizar",
        "sede": sede
    }

    return render(request, "sedes/formulario_sede.html", contexto)


# Eliminar una sede
def eliminar_sede(request, id):
    sede = get_object_or_404(Sede, pk=id)

    if request.method == "POST":
        nombre = sede.nombre
        sede.delete()

        messages.success(
            request,
            f"La sede '{nombre}' se eliminó correctamente."
        )

        return redirect("listar_sedes")

    return render(
        request,
        "gimnasios/eliminar_sede.html",
        {"sede": sede}
    )