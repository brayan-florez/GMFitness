import logging

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AlimentoForm
from .models import Alimento

logger = logging.getLogger(__name__)


# Listar todos los alimentos
def listar_alimentos(request):
    alimentos = Alimento.objects.all().order_by("nombre")
    return render(
        request,
        "alimentos/listar_alimentos.html",
        {"alimentos": alimentos}
    )


# Registrar un alimento
def crear_alimento(request):
    if request.method == "POST":
        form = AlimentoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El alimento se registró correctamente.")
                return redirect("listar_alimentos")
            except IntegrityError:
                form.add_error(None, "Ya existe un alimento con ese nombre.")
            except Exception:
                logger.exception("Error al registrar un alimento")
                form.add_error(None, "No fue posible registrar el alimento. Inténtalo de nuevo.")
    else:
        form = AlimentoForm()

    return render(
        request,
        "alimentos/formulario_alimento.html",
        {"form": form, "titulo": "Registrar alimento", "boton": "Guardar"}
    )


# Editar un alimento
def editar_alimento(request, id):
    alimento = get_object_or_404(Alimento, pk=id)

    if request.method == "POST":
        form = AlimentoForm(request.POST, request.FILES, instance=alimento)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El alimento se actualizó correctamente.")
                return redirect("listar_alimentos")
            except IntegrityError:
                form.add_error(None, "Ya existe un alimento con ese nombre.")
            except Exception:
                logger.exception("Error al actualizar el alimento %s", id)
                form.add_error(None, "No fue posible actualizar el alimento. Inténtalo de nuevo.")
    else:
        form = AlimentoForm(instance=alimento)

    return render(
        request,
        "alimentos/formulario_alimento.html",
        {
            "form": form,
            "titulo": "Editar alimento",
            "boton": "Actualizar",
            "alimento": alimento,
        }
    )


# Eliminar un alimento sin borrar sus comidas relacionadas
def eliminar_alimento(request, id):
    alimento = get_object_or_404(Alimento, pk=id)

    if request.method == "POST":
        try:
            if alimento.comidas.exists():
                messages.error(
                    request,
                    "No se puede eliminar este alimento porque está incluido "
                    "en una o más comidas."
                )
                return redirect("listar_alimentos")

            nombre = alimento.nombre
            alimento.delete()
            messages.success(
                request,
                f"El alimento '{nombre}' se eliminó correctamente."
            )
        except IntegrityError:
            messages.error(request, "No se pudo eliminar el alimento porque tiene registros relacionados.")
        except Exception:
            logger.exception("Error al eliminar el alimento %s", id)
            messages.error(request, "No fue posible eliminar el alimento. Inténtalo de nuevo.")
        return redirect("listar_alimentos")

    return render(
        request,
        "alimentos/eliminar_alimento.html",
        {"alimento": alimento}
    )


