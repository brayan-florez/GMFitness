from django.db import migrations


OBJETIVOS = (
    ("Perder peso", "Reducir peso corporal de forma progresiva."),
    ("Ganar masa muscular", "Aumentar masa muscular."),
    ("Aumentar fuerza", "Mejorar la fuerza física."),
    ("Mejorar resistencia", "Mejorar la resistencia física."),
    ("Mantener peso", "Mantener el peso corporal actual."),
    ("Mejorar condición física", "Mejorar la condición física general."),
    ("Otro", "Objetivo personalizado."),
)


def crear_objetivos(apps, schema_editor):
    Objetivo = apps.get_model("clientes", "Objetivo")
    db = schema_editor.connection.alias
    for nombre, descripcion in OBJETIVOS:
        Objetivo.objects.using(db).get_or_create(
            nombre=nombre,
            defaults={"descripcion": descripcion, "activo": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0003_medicionfisica_brazo_medicionfisica_muslo_and_more"),
    ]

    operations = [
        migrations.RunPython(crear_objetivos, migrations.RunPython.noop),
    ]
