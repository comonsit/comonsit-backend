# Generated by Django 2.2.7 on 2022-02-07 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_auto_20210417_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcredito',
            name='tipo_credito',
            field=models.CharField(choices=[('MC', 'Microcrédito'), ('CP', 'Crédito Productivo'), ('FC', 'Fondo Común')], max_length=2),
        ),
    ]
