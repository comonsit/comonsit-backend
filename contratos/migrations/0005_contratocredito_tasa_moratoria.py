# Generated by Django 2.2.7 on 2020-04-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0004_auto_20200413_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratocredito',
            name='tasa_moratoria',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=7),
            preserve_default=False,
        ),
    ]
