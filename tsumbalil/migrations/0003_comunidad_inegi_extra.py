# Generated by Django 2.2.7 on 2020-10-07 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ermitas', '0001_initial'),
        ('tsumbalil', '0002_comunidad_ermita'),
    ]

    operations = [
        migrations.AddField(
            model_name='comunidad',
            name='inegi_extra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ermitas.InegiLocalidad'),
        ),
    ]