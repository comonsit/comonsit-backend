# Generated by Django 2.2.7 on 2020-12-17 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bancos', '0003_auto_20201217_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientobanco',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimiento_banco', to=settings.AUTH_USER_MODEL),
        ),
    ]