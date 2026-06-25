from django.db import migrations


def crear_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Asegurar que existan los content types y permisos estándar
    modelos = [
        ('receta',         ['add', 'change', 'delete', 'view']),
        ('ingrediente',    ['add', 'change', 'delete', 'view']),
        ('pasoinstruccion',['add', 'change', 'delete', 'view']),
        ('etiqueta',       ['add', 'change', 'delete', 'view']),
        ('categoria',      ['add', 'change', 'delete', 'view']),
    ]
    for model_name, acciones in modelos:
        ct, _ = ContentType.objects.get_or_create(app_label='Landing', model=model_name)
        for accion in acciones:
            Permission.objects.get_or_create(
                content_type=ct,
                codename=f'{accion}_{model_name}',
                defaults={'name': f'Can {accion} {model_name}'},
            )

    # Permiso personalizado para gestionar cualquier receta
    receta_ct, _ = ContentType.objects.get_or_create(app_label='Landing', model='receta')
    Permission.objects.get_or_create(
        content_type=receta_ct,
        codename='can_manage_all_recetas',
        defaults={'name': 'Puede gestionar cualquier receta'},
    )

    # --- Grupo Cocinero ---
    # Puede crear y gestionar sus propias recetas. Solo visualiza etiquetas y categorías.
    cocinero_codenames = [
        'add_receta', 'change_receta', 'delete_receta', 'view_receta',
        'add_ingrediente', 'change_ingrediente', 'delete_ingrediente', 'view_ingrediente',
        'add_pasoinstruccion', 'change_pasoinstruccion', 'delete_pasoinstruccion', 'view_pasoinstruccion',
        'view_etiqueta',
        'view_categoria',
    ]

    # --- Grupo Editor ---
    # Extiende Cocinero: CRUD de etiquetas, categorías y gestión de todas las recetas.
    editor_codenames = cocinero_codenames + [
        'add_etiqueta', 'change_etiqueta', 'delete_etiqueta',
        'add_categoria', 'change_categoria', 'delete_categoria',
        'can_manage_all_recetas',
    ]

    cocinero, _ = Group.objects.get_or_create(name='Cocinero')
    cocinero.permissions.set(Permission.objects.filter(codename__in=cocinero_codenames))

    editor, _ = Group.objects.get_or_create(name='Editor')
    editor.permissions.set(Permission.objects.filter(codename__in=editor_codenames))


def eliminar_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Cocinero', 'Editor']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('Landing', '0003_receta_permisos'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(crear_grupos, eliminar_grupos),
    ]
