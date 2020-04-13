# Generated by Django 2.2.7 on 2020-04-10 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contratos', '0002_auto_20200407_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('folio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pago', models.DateField()),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fecha_banco', models.DateField(blank=True, null=True)),
                ('referencia_banco', models.CharField(blank=True, max_length=20, null=True)),
                ('interes_ord', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('interes_mor', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pago_autor', to=settings.AUTH_USER_MODEL)),
                ('credito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pago', to='contratos.ContratoCredito')),
            ],
        ),
    ]