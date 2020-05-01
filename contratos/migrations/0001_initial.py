# Generated by Django 2.2.7 on 2020-05-01 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socios', '0001_initial'),
        ('solicitudes', '0002_auto_20200421_0103'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=9)),
                ('plazo', models.PositiveSmallIntegerField()),
                ('tasa', models.DecimalField(decimal_places=4, max_digits=7)),
                ('tasa_moratoria', models.DecimalField(decimal_places=4, max_digits=7)),
                ('tipo_tasa', models.CharField(choices=[('FI', 'Fija'), ('VA', 'Variable')], max_length=2)),
                ('prorroga', models.PositiveSmallIntegerField(default=0)),
                ('estatus', models.CharField(choices=[('DP', 'Deuda Pendiente'), ('PA', 'Pagado')], max_length=2)),
                ('referencia_banco', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_salida_banco', models.DateField(blank=True, null=True)),
                ('estatus_ejecucion', models.CharField(choices=[('CO', 'Cobrado'), ('PC', 'Por cobrar'), ('CA', 'Cancelado')], max_length=2)),
                ('clave_socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrato', to='socios.Socio')),
                ('solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contrato', to='solicitudes.SolicitudCredito')),
            ],
        ),
    ]
