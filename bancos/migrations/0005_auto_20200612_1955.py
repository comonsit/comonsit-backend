# Generated by Django 2.2.7 on 2020-06-12 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0004_banco_clabe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocontable',
            name='aport_retiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movimientos.Movimiento'),
        ),
        migrations.AlterField(
            model_name='registrocontable',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pagos.Pago'),
        ),
    ]
