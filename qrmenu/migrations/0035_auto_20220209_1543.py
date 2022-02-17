# Generated by Django 3.2.7 on 2022-02-09 10:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0034_auto_20220209_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurantdetail',
            name='pack',
        ),
        migrations.AddField(
            model_name='pack',
            name='restaurant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='qrmenu.restaurantdetail'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 9, 15, 43, 51, 649639)),
        ),
    ]