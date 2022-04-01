# Generated by Django 3.2.7 on 2021-11-24 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('desc', models.TextField(null=True)),
                ('location', models.CharField(max_length=30, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('logo', models.ImageField(null=True, upload_to='')),
                ('menu_count', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]
