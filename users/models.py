from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен подтверждения")
    objects = UserManager()

@property
def is_manager(self):
    return self.groups.filter(name='managers').exists()
