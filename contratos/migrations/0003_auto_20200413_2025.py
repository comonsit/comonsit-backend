# Generated by Django 2.2.7 on 2020-04-13 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0002_auto_20200407_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratocredito',
            name='prorroga',
        ),
        migrations.AddField(
            model_name='contratocredito',
            name='prorroga',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]