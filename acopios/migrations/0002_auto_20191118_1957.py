# Generated by Django 2.2.7 on 2019-11-18 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acopios', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acopios',
            old_name='kilosDeProducto',
            new_name='kilos_de_producto',
        ),
        migrations.RenameField(
            model_name='acopios',
            old_name='tipoDeProducto',
            new_name='tipo_de_producto',
        ),
    ]
