# Generated by Django 2.2.7 on 2020-03-29 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movimientos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimiento_autor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='clave_socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimiento', to='socios.Socio'),
        ),
    ]
