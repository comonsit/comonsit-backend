# Generated by Django 2.2.7 on 2020-08-18 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contratos', '0001_initial'),
        ('pagos', '0001_initial'),
        ('movimientos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='registrocontable',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pagos.Pago'),
        ),
        migrations.AddField(
            model_name='registrocontable',
            name='subcuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bancos.SubCuenta'),
        ),
        migrations.AddField(
            model_name='movimientobanco',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimiento_banco', to=settings.AUTH_USER_MODEL),
        ),
    ]
