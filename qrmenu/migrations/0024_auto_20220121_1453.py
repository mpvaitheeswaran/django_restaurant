# Generated by Django 3.2.7 on 2022-01-21 09:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0006_increase_name_max_length'),
        ('qrmenu', '0023_auto_20220121_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsetting',
            name='currency_model',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.currency'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 21, 14, 53, 14, 824752)),
        ),
    ]
