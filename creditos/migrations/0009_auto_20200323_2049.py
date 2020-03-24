# Generated by Django 2.2.7 on 2020-03-23 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('creditos', '0008_remove_solicitudcredito_estatus_ej_credito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudcredito',
            name='comentarios_coordinador',
        ),
        migrations.RemoveField(
            model_name='solicitudcredito',
            name='comentarios_gerente',
        ),
        migrations.RemoveField(
            model_name='solicitudcredito',
            name='comentarios_promotor',
        ),
        migrations.RemoveField(
            model_name='solicitudcredito',
            name='coordinador',
        ),
        migrations.CreateModel(
            name='ChatSolicitudCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='creditos.SolicitudCredito')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_solic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
