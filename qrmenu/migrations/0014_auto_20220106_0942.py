# Generated by Django 3.2.7 on 2022-01-06 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrmenu', '0013_auto_20220105_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingdetail',
            name='country',
            field=models.CharField(choices=[('india', 'India'), ('usa', 'United State of America'), ('uae', 'United Arab Emirates'), ('uk', 'United Kingdom')], default=('india', 'India'), max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='billingdetail',
            name='restaurant',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='qrmenu.restaurantdetail'),
        ),
    ]
