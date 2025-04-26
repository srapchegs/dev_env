from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    otchestvo = models.TextField(default="")

    class Meta:
        db_table = 'users'
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"