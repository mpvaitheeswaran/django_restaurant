# Generated by Django 2.1.15 on 2022-04-01 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0049_auto_20220401_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 16, 38, 27, 626000)),
        ),
    ]