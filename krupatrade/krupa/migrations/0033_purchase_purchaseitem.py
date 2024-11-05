# Generated by Django 5.1 on 2024-11-04 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0032_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_supply', models.CharField(blank=True, max_length=255, null=True)),
                ('destination_of_supply', models.CharField(blank=True, max_length=255, null=True)),
                ('bill', models.CharField(blank=True, max_length=255, null=True)),
                ('order_number', models.CharField(blank=True, max_length=255, null=True)),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('payment_terms', models.CharField(blank=True, max_length=255, null=True)),
                ('item_tax', models.CharField(blank=True, max_length=50, null=True)),
                ('price_list', models.CharField(blank=True, max_length=50, null=True)),
                ('discount', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shipping_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('adjustment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_details', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tax', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='krupa.invoice')),
            ],
        ),
    ]
