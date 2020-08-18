# Generated by Django 2.2.7 on 2020-08-18 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_banco', models.CharField(max_length=40)),
                ('nombre_cuenta', models.CharField(max_length=40)),
                ('numero_cuenta', models.CharField(max_length=100)),
                ('clabe', models.CharField(blank=True, max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoBanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia_banco', models.CharField(max_length=20, unique=True)),
                ('fecha', models.DateField()),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('referencia_alf', models.CharField(blank=True, max_length=60, null=True)),
                ('fecha_auto', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroContable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ingr_egr', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('id_contable', models.CharField(max_length=40)),
                ('tipo', models.CharField(choices=[('IN', 'Ingreso'), ('EG', 'Egreso'), ('IE', 'Ingreso/Egreso')], max_length=2)),
                ('sistema', models.BooleanField(blank=True, default=True)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcuenta', to='bancos.Banco')),
            ],
        ),
    ]
