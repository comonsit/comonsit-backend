# Generated by Django 2.2.7 on 2020-06-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0003_auto_20200609_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='banco',
            name='clabe',
            field=models.CharField(blank=True, max_length=18),
        ),
    ]