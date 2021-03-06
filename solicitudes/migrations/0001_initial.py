# Generated by Django 2.2.7 on 2020-12-17 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSolicitudCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudCredito',
            fields=[
                ('folio_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_solicitud', models.DateField()),
                ('proceso', models.CharField(choices=[('CF', 'Café'), ('MI', 'Miel'), ('JA', 'Jabon'), ('SL', 'Sueldos')], max_length=2)),
                ('tipo_credito', models.CharField(choices=[('MC', 'Microcrédito'), ('CP', 'Crédito Productivo')], max_length=2)),
                ('act_productiva', models.CharField(blank=True, choices=[('CA', 'Cafetal'), ('VI', 'Viveros'), ('HR', 'Hortalizas'), ('GE', 'Ganado Vacuno (engorda)'), ('GC', 'Ganado Vacuno (pie de cría)'), ('PE', 'Ganado Porcino (engorda)'), ('PC', 'Ganado Porcino (pie de cría)'), ('AT', 'Aves de Traspatio'), ('MI', 'Milpa'), ('EL', 'Elaboración de Alimentos'), ('ER', 'Elaboración de Artesanía'), ('HE', 'Herramientas y Equipo de Trabajo'), ('OT', 'Otro')], max_length=2)),
                ('act_productiva_otro', models.CharField(blank=True, max_length=40, null=True)),
                ('mot_credito', models.CharField(choices=[('SA', 'Salud'), ('AL', 'Alimento'), ('TR', 'Trabajo'), ('ED', 'Educación'), ('FI', 'Fiestas'), ('OT', 'Otro')], max_length=2)),
                ('mot_credito_otro', models.CharField(blank=True, max_length=30, null=True)),
                ('emergencia_medica', models.BooleanField(default=False)),
                ('monto_solicitado', models.DecimalField(decimal_places=2, max_digits=9)),
                ('plazo_de_pago_solicitado', models.PositiveSmallIntegerField()),
                ('estatus_solicitud', models.CharField(choices=[('AP', 'Aprobado'), ('RV', 'Revisión'), ('RE', 'Rechazado'), ('CA', 'Cancelado')], max_length=2)),
                ('estatus_evaluacion', models.CharField(choices=[('AP', 'Aprobado'), ('RV', 'Revisión'), ('NE', 'Negociación'), ('CA', 'Cancelado')], max_length=2)),
                ('justificacion_credito', models.CharField(max_length=100)),
                ('pregunta_1', models.BooleanField(default=None, null=True)),
                ('pregunta_2', models.BooleanField(default=None, null=True)),
                ('pregunta_3', models.BooleanField(default=None, null=True)),
                ('pregunta_4', models.BooleanField(default=None, null=True)),
                ('irregularidades', models.CharField(blank=True, max_length=100)),
                ('familiar_responsable', models.CharField(max_length=100)),
                ('aval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aval', to='socios.Socio')),
                ('clave_socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitud', to='socios.Socio')),
            ],
        ),
    ]
