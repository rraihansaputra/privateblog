from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AppUser(AbstractUser):
    # custom user model to accomodate future changes
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    # uid = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username
