from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver

class Managers(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    displayname = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    work_phone = models.CharField(max_length=12)
    emergency_phone = models.CharField(max_length=12,null=True,blank=True)

    def __str__(self):
        return self.displayname