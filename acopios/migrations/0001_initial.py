# Generated by Django 2.2.7 on 2020-06-09 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acopio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('ingreso', models.DecimalField(decimal_places=2, max_digits=8)),
                ('kilos_de_producto', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('tipo_de_producto', models.CharField(blank=True, choices=[('CF', 'Café'), ('MI', 'Miel'), ('JA', 'Jabon'), ('SL', 'Sueldos')], max_length=2)),
                ('clave_socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acopio', to='socios.Socio')),
            ],
        ),
    ]
