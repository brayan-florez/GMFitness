from django.db import migrations


PLANES = (
    ("BASICO", "Básico"),
    ("PREMIUM", "Premium"),
    ("BLACK", "Black"),
)


def crear_planes(apps, schema_editor):
    Sede = apps.get_model("gimnasios", "Sede")
    PlanMembresia = apps.get_model("membresias", "PlanMembresia")
    db = schema_editor.connection.alias
    for sede in Sede.objects.using(db).all():
        for nivel, nombre in PLANES:
            PlanMembresia.objects.using(db).get_or_create(
                sede_id=sede.pk,
                nivel=nivel,
                defaults={"nombre": nombre, "activo": True},
            )


class Migration(migrations.Migration):
    dependencies = [
        ("membresias", "0002_remove_planmembresia_plan_nombre_unico_por_sede_and_more"),
    ]

    operations = [
        migrations.RunPython(crear_planes, migrations.RunPython.noop),
    ]
