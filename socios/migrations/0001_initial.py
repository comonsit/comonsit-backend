# Generated by Django 2.2.7 on 2020-03-29 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tsumbalil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('clave_socio', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('curp', models.CharField(blank=True, max_length=18, verbose_name='CURP')),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_ingr_yomol_atel', models.DateField()),
                ('fecha_ingr_programa', models.DateField()),
                ('clave_anterior', models.CharField(blank=True, max_length=10, null=True)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino'), ('OT', 'Otro')], max_length=2)),
                ('estatus_cafe', models.CharField(choices=[('AC', 'Activo'), ('NP', 'No Participa'), ('BA', 'Baja')], max_length=2)),
                ('estatus_miel', models.CharField(choices=[('AC', 'Activo'), ('NP', 'No Participa'), ('BA', 'Baja')], max_length=2)),
                ('estatus_yip', models.CharField(choices=[('AC', 'Activo'), ('NP', 'No Participa'), ('BA', 'Baja')], max_length=2)),
                ('estatus_trabajador', models.CharField(choices=[('AC', 'Activo'), ('NP', 'No Participa'), ('BA', 'Baja')], max_length=2)),
                ('estatus_comonSit', models.CharField(choices=[('AC', 'Activo'), ('NP', 'No Participa'), ('BA', 'Baja')], max_length=2)),
                ('doc_curp', models.BooleanField(default=False)),
                ('doc_act_nac', models.BooleanField(default=False)),
                ('doc_ine', models.BooleanField(default=False)),
                ('doc_domicilio', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tsumbalil.Cargo')),
                ('cargo_coop', models.ManyToManyField(blank=True, default=1, related_name='Socio_cargo_coop', to='tsumbalil.CargoCoop')),
                ('comunidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tsumbalil.Comunidad')),
                ('empresa', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsumbalil.Empresa')),
                ('fuente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Socio_fuente', to='tsumbalil.Fuente')),
                ('puesto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Socio_puesto', to='tsumbalil.Puesto_Trabajo')),
            ],
        ),
    ]
