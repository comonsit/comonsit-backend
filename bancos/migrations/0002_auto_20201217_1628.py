# Generated by Django 2.2.7 on 2020-12-17 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movimientos', '0001_initial'),
        ('contratos', '0001_initial'),
        ('bancos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrocontable',
            name='aport_retiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movimientos.Movimiento'),
        ),
        migrations.AddField(
            model_name='registrocontable',
            name='ej_credito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratos.ContratoCredito'),
        ),
        migrations.AddField(
            model_name='registrocontable',
            name='movimiento_banco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bancos.MovimientoBanco'),
        ),
    ]