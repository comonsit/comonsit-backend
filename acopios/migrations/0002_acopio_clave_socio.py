# Generated by Django 2.2.7 on 2020-01-24 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0004_socio_empresa'),
        ('acopios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='acopio',
            name='clave_socio',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='acopio', to='socios.Socio'),
            preserve_default=False,
        ),
    ]