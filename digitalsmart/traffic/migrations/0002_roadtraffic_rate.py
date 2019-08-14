# Generated by Django 2.2.3 on 2019-08-14 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadtraffic',
            name='rate',
            field=models.FloatField(db_column='rate', default=0, verbose_name='最近交通拥堵指数'),
            preserve_default=False,
        ),
    ]
