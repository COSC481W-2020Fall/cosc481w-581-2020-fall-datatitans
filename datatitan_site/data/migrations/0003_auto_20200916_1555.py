# Generated by Django 2.2.16 on 2020-09-16 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pyblished_date',
            new_name='published_date',
        ),
    ]
