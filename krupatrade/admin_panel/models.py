from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from krupa.models import *
from krupa.models import CustomUser

class Managers(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    displayname = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    work_phone = models.CharField(max_length=12)
    emergency_phone = models.CharField(max_length=12,null=True,blank=True)

    def __str__(self):
        return self.displayname
    

class Estimates(models.Model):
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    place_of_supply = models.CharField(max_length=30,null=True,blank=True)
    estimate_date = models.DateField(null=True,blank=True)
    expiry_date = models.DateField(null=True,blank=True)
    sales_person = models.CharField(max_length=30,null=True,blank=True)
    project_name = models.CharField(max_length=30,null=True,blank=True)
    subject = models.TextField(null=True,blank=True)
    shipping = models.IntegerField(null=True,blank=True)
    adjustments = models.IntegerField(null=True,blank=True)
    customer_notes = models.TextField(null=True,blank=True)
    conditions = models.TextField(null=True,blank=True)