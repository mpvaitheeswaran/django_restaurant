# Generated by Django 3.2.7 on 2022-01-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0018_billingdetail_gstin'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='status',
            field=models.CharField(default='pending', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='success',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='restaurantdetail',
            name='image',
            field=models.ImageField(default='default/default.png', null=True, upload_to='restaurant_image'),
        ),
        migrations.AlterField(
            model_name='restaurantdetail',
            name='logo',
            field=models.ImageField(default='default/default.png', null=True, upload_to='restaurant_logo'),
        ),
    ]
