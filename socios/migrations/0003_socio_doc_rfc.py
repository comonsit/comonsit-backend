# Generated by Django 2.2.7 on 2020-10-23 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0002_auto_20201023_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='doc_rfc',
            field=models.BooleanField(default=False),
        ),
    ]
