# Generated by Django 2.1.15 on 2022-04-07 04:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0053_auto_20220401_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucategory',
            name='name_ar',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='menucategory',
            name='name_en_us',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='menucategory',
            name='name_ta',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='name_ar',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='name_en_us',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='name_ta',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='accountsetting',
            name='menu_language',
            field=models.CharField(blank=True, choices=[('en-us', 'English'), ('ta', 'Tamil'), ('ar', 'Arabic')], default='en-us', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 10, 29, 11, 181973)),
        ),
    ]
