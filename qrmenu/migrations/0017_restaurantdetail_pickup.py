# Generated by Django 3.2.7 on 2022-01-07 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0016_auto_20220106_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantdetail',
            name='pickup',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
