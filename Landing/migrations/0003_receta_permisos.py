from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Landing', '0002_etiqueta_receta_etiquetas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receta',
            options={
                'permissions': [
                    ('can_manage_all_recetas', 'Puede gestionar cualquier receta'),
                ],
            },
        ),
    ]
