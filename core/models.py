import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserType(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
