from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=244, unique=False)
    email = models.EmailField(max_length=86, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name