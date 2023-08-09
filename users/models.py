from django.contrib.auth.models import AbstractUser
from django.db import models
from dogs.models import NULLABLE


class User(AbstractUser):
    age = models.PositiveIntegerField(**NULLABLE)
