# Generated by Django 5.1 on 2024-10-10 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0011_request_type_alter_products_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
