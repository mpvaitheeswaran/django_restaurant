# Generated by Django 3.2.7 on 2022-03-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20220314_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='packorder',
            name='invoice_pdf',
            field=models.FileField(blank=True, null=True, upload_to='invoice_pdfs'),
        ),
    ]
