# Generated by Django 2.2.7 on 2020-10-22 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsumbalil', '0003_comunidad_inegi_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comunidad',
            name='nombre_de_comunidad',
            field=models.CharField(max_length=50),
        ),
    ]