# Generated by Django 2.2.7 on 2021-03-24 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0004_auto_20210324_0047'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pagos', '0002_auto_20201217_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condonacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_condonacion', models.DateField()),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('interes_ord', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('interes_mor', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('estatus_previo', models.CharField(choices=[('VI', 'Vigente'), ('VE', 'Vencido')], max_length=2)),
                ('justificacion', models.CharField(max_length=100)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='condonacion_autor', to=settings.AUTH_USER_MODEL)),
                ('credito', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='condonacion', to='contratos.ContratoCredito')),
            ],
        ),
    ]