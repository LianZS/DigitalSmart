# Generated by Django 2.2.3 on 2019-07-24 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadtraffic',
            name='bounds',
            field=models.TextField(db_column='bound', verbose_name='经纬度列表字符串'),
        ),
    ]
