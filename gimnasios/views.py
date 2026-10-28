import logging

from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Sede
from .forms import SedeForm

logger = logging.getLogger(__name__)


def inicio(request):
    """Página principal con acceso a los módulos de GMFitness."""
    return render(request, "inicio.html")


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
            try:
                form.save()
                messages.success(request, "La sede se registró correctamente.")
                return redirect("listar_sedes")
            except IntegrityError:
                form.add_error(None, "Ya existe una sede con esos datos.")
            except Exception:
                logger.exception("Error al registrar una sede")
                form.add_error(None, "No fue posible registrar la sede. Inténtalo de nuevo.")

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
            try:
                form.save()
                messages.success(request, "La sede se actualizó correctamente.")
                return redirect("listar_sedes")
            except IntegrityError:
                form.add_error(None, "Ya existe una sede con esos datos.")
            except Exception:
                logger.exception("Error al actualizar la sede %s", id)
                form.add_error(None, "No fue posible actualizar la sede. Inténtalo de nuevo.")

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
        try:
            sede.delete()
            messages.success(
                request,
                f"La sede '{nombre}' se eliminó correctamente."
            )
        except IntegrityError:
            messages.error(request, "No se pudo eliminar la sede porque tiene registros relacionados.")
        except Exception:
            logger.exception("Error al eliminar la sede %s", id)
            messages.error(request, "No fue posible eliminar la sede. Inténtalo de nuevo.")
        return redirect("listar_sedes")

    return render(
        request,
        "sedes/eliminar_sede.html",
        {"sede": sede}
    )
