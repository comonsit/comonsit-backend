# Generated by Django 2.2.7 on 2020-03-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditos', '0010_auto_20200326_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcredito',
            name='proceso',
            field=models.CharField(choices=[('CF', 'Café'), ('MI', 'Miel'), ('JA', 'Jabon'), ('SL', 'Sueldos')], max_length=2),
        ),
    ]
