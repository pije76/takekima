from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, User, Permission, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
)

# Create your models here.
class Profile(AbstractUser):
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male', blank=False, null=False)

    def __str__(self):
        return self.username
