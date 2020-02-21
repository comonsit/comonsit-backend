# Generated by Django 2.2.7 on 2020-02-21 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('creditos', '0005_solicitudcredito_comentarios_gerente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudcredito',
            name='autor',
        ),
        migrations.AddField(
            model_name='solicitudcredito',
            name='coordinador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solic_coord', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solicitudcredito',
            name='promotor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='solic_promotor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
