from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    date_birth = models.DateField(blank=True, null=True)


