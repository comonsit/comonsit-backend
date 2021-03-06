# Generated by Django 2.2.7 on 2020-12-17 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_entrega', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=9)),
                ('proceso', models.CharField(choices=[('CF', 'Café'), ('MI', 'Miel'), ('JA', 'Jabon'), ('SL', 'Sueldos')], default='CF', max_length=2)),
                ('aportacion', models.BooleanField(default=True)),
                ('ordinario', models.BooleanField(blank=True, default=True, null=True)),
                ('tipo_de_movimiento', models.CharField(choices=[('EF', 'Efectivo'), ('BA', 'Bancos'), ('TR', 'Transferencia')], max_length=2)),
                ('responsable_entrega', models.CharField(blank=True, max_length=50)),
                ('fecha_banco', models.DateField(blank=True, null=True)),
                ('referencia_banco', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
