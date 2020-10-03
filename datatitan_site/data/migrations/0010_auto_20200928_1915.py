# Generated by Django 3.1.1 on 2020-09-28 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20200922_1919'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='coviddataraw',
            index=models.Index(fields=['iso_code', 'date'], name='data_covidd_iso_cod_b90079_idx'),
        ),
    ]
