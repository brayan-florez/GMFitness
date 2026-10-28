import logging
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotAllowed
from django.urls import path, reverse
from django.db.models import Q


logger = logging.getLogger(__name__)


def _form_class(model, supplied_form, exclude):
    if supplied_form is not None:
        return supplied_form
    return modelform_factory(model, fields="__all__", exclude=exclude or ())


def _read_path(obj, path):
    value = obj
    for part in path.split("__"):
        if value is None:
            return "—"
        value = getattr(value, part, None)
    return value if value not in (None, "") else "—"


def _label(model, path):
    try:
        field = model._meta.get_field(path.split("__")[-1])
        return str(field.verbose_name).capitalize()
    except Exception:
        return path.replace("__", " ").replace("_", " ").capitalize()


def _search(queryset, fields, term):
    if not term or not fields:
        return queryset
    expression = Q()
    for field in fields:
        expression |= Q(**{f"{field}__icontains": term})
    return queryset.filter(expression)


def _list_view(model, title, names, search_fields, display_fields, queryset, soft_delete_field, action, read_only, delete_label):
    def view(request):
        objects = queryset() if callable(queryset) else queryset
        if objects is None:
            objects = model._default_manager.all()
        term = request.GET.get("q", "").strip()
        objects = _search(objects, search_fields, term)
        fields = display_fields or ("id",)
        columns = [_label(model, field) for field in fields]
        rows = []
        for obj in objects:
            cells = []
            for field in fields:
                if field.endswith("_display"):
                    display = getattr(obj, f"get_{field[:-8]}_display", None)
                    value = display() if display else _read_path(obj, field[:-8])
                else:
                    value = _read_path(obj, field.replace(".", "__"))
                cells.append(value)
            rows.append({
                "object": obj,
                "cells": cells,
                "edit_url": reverse(names["edit"], args=(obj.pk,)) if not read_only else None,
                "delete_url": reverse(names["delete"], args=(obj.pk,)) if not read_only else None,
                "action_url": reverse(names["action"], args=(obj.pk,)) if action else None,
                "show_action": bool(
                    action
                    and (
                        not action.get("condition_field")
                        or getattr(obj, action["condition_field"]) == action.get("condition_value")
                    )
                ),
            })
        return render(request, "crud/list.html", {
            "title": title,
            "columns": columns,
            "rows": rows,
            "create_url": reverse(names["create"]) if not read_only else None,
            "list_url": reverse(names["list"]),
            "query": term,
            "soft_delete": bool(soft_delete_field),
            "delete_label": delete_label or ("Desactivar" if soft_delete_field else "Eliminar"),
            "action_label": action.get("label") if action else None,
            "read_only": read_only,
        })
    view.__name__ = names["list"]
    return view


def _form_view(model, title, names, form_class, exclude, instance_id=None):
    def view(request, pk=None):
        instance = get_object_or_404(model, pk=pk) if pk is not None else None
        action = "Editar" if instance is not None else "Crear"
        form_type = form_class
        if isinstance(form_type, tuple):
            form_type = form_type[1 if instance is not None else 0]
        form_type = _form_class(model, form_type, exclude)
        form = form_type(
            request.POST if request.method == "POST" else None,
            request.FILES if request.method == "POST" else None,
            instance=instance,
        )
        if request.method == "POST" and form.is_valid():
            try:
                with transaction.atomic():
                    saved = form.save()
                messages.success(request, f"{title} se guardó correctamente.")
                return redirect(names["list"])
            except IntegrityError:
                form.add_error(None, "No se pudo guardar por un registro duplicado o relacionado.")
            except ValidationError as error:
                form.add_error(None, error)
            except Exception:
                logger.exception("Error al guardar %s (id=%s)", title, pk)
                form.add_error(None, f"No fue posible guardar {title.lower()}. Inténtalo de nuevo.")
        return render(request, "crud/form.html", {
            "title": f"{action} {title.lower()}",
            "form": form,
            "list_url": reverse(names["list"]),
            "button": "Actualizar" if instance is not None else "Guardar",
        })
    view.__name__ = names["edit"] if instance_id is not None else names["create"]
    return view


def _delete_view(model, title, names, soft_delete_field, soft_delete_value=None, delete_label=None):
    def view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            try:
                if soft_delete_field:
                    value = soft_delete_value if soft_delete_value is not None else False
                    setattr(obj, soft_delete_field, value)
                    obj.save(update_fields=(soft_delete_field,))
                    messages.success(request, f"{title} se desactivó correctamente.")
                else:
                    obj.delete()
                    messages.success(request, f"{title} se eliminó correctamente.")
            except IntegrityError:
                messages.error(request, f"No se puede eliminar {title.lower()} porque tiene registros relacionados.")
            except Exception:
                logger.exception("Error al eliminar %s (id=%s)", title, pk)
                messages.error(request, f"No fue posible eliminar {title.lower()}. Inténtalo de nuevo.")
            return redirect(names["list"])
        return render(request, "crud/delete.html", {
            "title": f"Eliminar {title.lower()}",
            "object": obj,
            "list_url": reverse(names["list"]),
            "button": delete_label or ("Desactivar" if soft_delete_field else "Confirmar eliminación"),
        })
    view.__name__ = names["delete"]
    return view


def _action_view(model, title, names, action):
    def view(request, pk):
        if request.method != "POST":
            return HttpResponseNotAllowed(("POST",))
        obj = get_object_or_404(model, pk=pk)
        try:
            getattr(obj, action["method"])()
            messages.success(request, f"Acción realizada para {title.lower()}.")
        except ValidationError as error:
            messages.error(request, error)
        except Exception:
            logger.exception("Error al ejecutar acción %s en %s (id=%s)", action["method"], title, pk)
            messages.error(request, f"No fue posible procesar {title.lower()}. Inténtalo de nuevo.")
        return redirect(names["list"])
    view.__name__ = names["action"]
    return view


def crud_patterns(
    model,
    prefix,
    title,
    *,
    route=None,
    search_fields=(),
    display_fields=(),
    form_class=None,
    exclude=(),
    queryset=None,
    soft_delete_field=None,
    soft_delete_value=None,
    delete_label=None,
    read_only=False,
    action=None,
):
    """Rutas CRUD basadas en vistas función, reutilizables por cada app."""
    route = route or prefix.replace("_", "-")
    names = {
        "list": f"listar_{prefix}",
        "create": f"crear_{prefix}",
        "edit": f"editar_{prefix}",
        "delete": f"eliminar_{prefix}",
        "action": f"accion_{prefix}",
    }
    patterns = [
        path(
            f"{route}/",
            _list_view(model, title, names, search_fields, display_fields, queryset, soft_delete_field, action, read_only, delete_label),
            name=names["list"],
        ),
        path(
            f"{route}/crear/",
            _form_view(model, title, names, form_class, exclude),
            name=names["create"],
        ),
        path(
            f"{route}/<int:pk>/editar/",
            _form_view(model, title, names, form_class, exclude, instance_id=True),
            name=names["edit"],
        ),
        path(
            f"{route}/<int:pk>/eliminar/",
            _delete_view(model, title, names, soft_delete_field, soft_delete_value, delete_label),
            name=names["delete"],
        ),
    ]
    if read_only:
        return patterns[:1]
    if action:
        patterns.append(path(
            f"{route}/<int:pk>/{action.get('route', 'accion')}/",
            _action_view(model, title, names, action),
            name=names["action"],
        ))
    return patterns
