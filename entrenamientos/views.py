import logging

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from usuarios.decorators import rol_requerido

from .forms import EjercicioForm
from .models import Ejercicio

logger = logging.getLogger(__name__)


@rol_requerido('ADMIN', 'ENTRENADOR')
# Listar todos los ejercicios
def listar_ejercicios(request):
    ejercicios = Ejercicio.objects.all().order_by("nombre")
    return render(
        request,
        "ejercicios/listar_ejercicios.html",
        {"ejercicios": ejercicios}
    )


@rol_requerido('ADMIN', 'ENTRENADOR')
# Registrar un ejercicio
def crear_ejercicio(request):
    if request.method == "POST":
        form = EjercicioForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El ejercicio se registró correctamente.")
                return redirect("listar_ejercicios")
            except IntegrityError:
                form.add_error(None, "Ya existe un ejercicio con ese nombre.")
            except Exception:
                logger.exception("Error al registrar un ejercicio")
                form.add_error(None, "No fue posible registrar el ejercicio. Inténtalo de nuevo.")
    else:
        form = EjercicioForm()

    return render(
        request,
        "ejercicios/formulario_ejercicio.html",
        {"form": form, "titulo": "Registrar ejercicio", "boton": "Guardar"}
    )


@rol_requerido('ADMIN', 'ENTRENADOR')
# Editar un ejercicio
def editar_ejercicio(request, id):
    ejercicio = get_object_or_404(Ejercicio, pk=id)

    if request.method == "POST":
        form = EjercicioForm(request.POST, request.FILES, instance=ejercicio)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El ejercicio se actualizó correctamente.")
                return redirect("listar_ejercicios")
            except IntegrityError:
                form.add_error(None, "Ya existe un ejercicio con ese nombre.")
            except Exception:
                logger.exception("Error al actualizar el ejercicio %s", id)
                form.add_error(None, "No fue posible actualizar el ejercicio. Inténtalo de nuevo.")
    else:
        form = EjercicioForm(instance=ejercicio)

    return render(
        request,
        "ejercicios/formulario_ejercicio.html",
        {
            "form": form,
            "titulo": "Editar ejercicio",
            "boton": "Actualizar",
            "ejercicio": ejercicio,
        }
    )


@rol_requerido('ADMIN', 'ENTRENADOR')
# Eliminar un ejercicio sin borrar sus rutinas relacionadas
def eliminar_ejercicio(request, id):
    ejercicio = get_object_or_404(Ejercicio, pk=id)

    if request.method == "POST":
        try:
            if ejercicio.rutinas.exists():
                messages.error(
                    request,
                    "No se puede eliminar este ejercicio porque está incluido "
                    "en una o más rutinas."
                )
                return redirect("listar_ejercicios")

            nombre = ejercicio.nombre
            ejercicio.delete()
            messages.success(
                request,
                f"El ejercicio '{nombre}' se eliminó correctamente."
            )
        except IntegrityError:
            messages.error(request, "No se pudo eliminar el ejercicio porque tiene registros relacionados.")
        except Exception:
            logger.exception("Error al eliminar el ejercicio %s", id)
            messages.error(request, "No fue posible eliminar el ejercicio. Inténtalo de nuevo.")
        return redirect("listar_ejercicios")

    return render(
        request,
        "ejercicios/eliminar_ejercicio.html",
        {"ejercicio": ejercicio}
    )
