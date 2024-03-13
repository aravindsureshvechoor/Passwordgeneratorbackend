from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserAccountManager


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]


class saved_password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50)
    password = models.BinaryField()


class secureKeys(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    s_key = models.BinaryField()
