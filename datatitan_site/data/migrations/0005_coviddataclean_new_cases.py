# Generated by Django 3.1.1 on 2020-09-22 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_remove_coviddataclean_new_cases'),
    ]

    operations = [
        migrations.AddField(
            model_name='coviddataclean',
            name='new_cases',
            field=models.IntegerField(default=0),
        ),
    ]