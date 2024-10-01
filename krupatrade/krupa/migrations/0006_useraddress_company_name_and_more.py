# Generated by Django 5.1 on 2024-09-09 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0005_useraddress_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='address_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='street_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]