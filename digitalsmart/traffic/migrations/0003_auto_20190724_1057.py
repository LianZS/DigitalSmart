# Generated by Django 2.2.3 on 2019-07-24 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0002_auto_20190724_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roadtraffic',
            old_name='bounds',
            new_name='bound',
        ),
    ]
