# Generated by Django 2.1.15 on 2022-04-01 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('qrmenu', '0049_auto_20220401_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackOrder',
            fields=[
                ('order_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('pack_type', models.CharField(max_length=5)),
                ('order_amount', models.CharField(max_length=25)),
                ('isPaid', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(blank=True, default='inr', max_length=5, null=True)),
                ('invoice_pdf', models.FileField(blank=True, null=True, upload_to='invoice_pdfs')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qrmenu.RestaurantDetail')),
            ],
            options={
                'ordering': ['-order_date'],
            },
        ),
    ]
