# Generated by Django 5.1 on 2024-09-29 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0008_orders_company_orders_quantity_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(blank=True, editable=False, max_length=10, unique=True),
        ),
    ]