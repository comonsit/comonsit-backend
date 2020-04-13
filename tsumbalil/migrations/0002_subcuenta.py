# Generated by Django 2.2.7 on 2020-04-10 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsumbalil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cuenta', models.CharField(max_length=40)),
                ('proceso', models.CharField(blank=True, choices=[('CF', 'Café'), ('MI', 'Miel'), ('JA', 'Jabon'), ('SL', 'Sueldos')], max_length=2, null=True)),
            ],
        ),
    ]