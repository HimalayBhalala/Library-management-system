from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLE_CHOICES = (
    ("Librarian","Librarian"),
    ("Student","Student")
)

class User(AbstractUser):
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

