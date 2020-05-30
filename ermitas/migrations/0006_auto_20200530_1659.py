# Generated by Django 3.0.6 on 2020-05-30 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ermitas', '0005_auto_20200525_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inegilocalidad',
            options={'ordering': ['municipio', 'nombre'], 'verbose_name': 'INEGI localidad', 'verbose_name_plural': 'INEGI localidades'},
        ),
        migrations.AddField(
            model_name='ermita',
            name='localidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ermitas.InegiLocalidad'),
        ),
        migrations.AddField(
            model_name='ermita',
            name='localidad_nota',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
