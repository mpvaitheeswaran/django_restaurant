# Generated by Django 3.2.7 on 2022-03-04 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0040_auto_20220302_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantdetail',
            name='is_free_pack_used',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 4, 13, 23, 54, 268936)),
        ),
        migrations.AlterField(
            model_name='pack',
            name='pack_type',
            field=models.IntegerField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='pack',
            name='total_scans',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
