# Generated by Django 2.2.7 on 2020-09-29 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0002_auto_20200911_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='ordinario',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
