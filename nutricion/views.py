from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AlimentoForm
from .models import Alimento


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
        form = AlimentoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "El alimento se registró correctamente.")
            return redirect("listar_alimentos")
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
        form = AlimentoForm(request.POST, instance=alimento)

        if form.is_valid():
            form.save()
            messages.success(request, "El alimento se actualizó correctamente.")
            return redirect("listar_alimentos")
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
        return redirect("listar_alimentos")

    return render(
        request,
        "alimentos/eliminar_alimento.html",
        {"alimento": alimento}
    )
