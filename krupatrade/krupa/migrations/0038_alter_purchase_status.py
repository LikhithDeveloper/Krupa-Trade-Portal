# Generated by Django 5.1 on 2024-11-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0037_purchase_created_date_purchase_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(blank=True, default='OPEN', max_length=30, null=True),
        ),
    ]
