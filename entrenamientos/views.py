from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EjercicioForm
from .models import Ejercicio


# Listar todos los ejercicios
def listar_ejercicios(request):
    ejercicios = Ejercicio.objects.all().order_by("nombre")
    return render(
        request,
        "ejercicios/listar_ejercicios.html",
        {"ejercicios": ejercicios}
    )


# Registrar un ejercicio
def crear_ejercicio(request):
    if request.method == "POST":
        form = EjercicioForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "El ejercicio se registró correctamente.")
            return redirect("listar_ejercicios")
    else:
        form = EjercicioForm()

    return render(
        request,
        "ejercicios/formulario_ejercicio.html",
        {"form": form, "titulo": "Registrar ejercicio", "boton": "Guardar"}
    )


# Editar un ejercicio
def editar_ejercicio(request, id):
    ejercicio = get_object_or_404(Ejercicio, pk=id)

    if request.method == "POST":
        form = EjercicioForm(request.POST, request.FILES, instance=ejercicio)

        if form.is_valid():
            form.save()
            messages.success(request, "El ejercicio se actualizó correctamente.")
            return redirect("listar_ejercicios")
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


# Eliminar un ejercicio sin borrar sus rutinas relacionadas
def eliminar_ejercicio(request, id):
    ejercicio = get_object_or_404(Ejercicio, pk=id)

    if request.method == "POST":
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
        return redirect("listar_ejercicios")

    return render(
        request,
        "ejercicios/eliminar_ejercicio.html",
        {"ejercicio": ejercicio}
    )
