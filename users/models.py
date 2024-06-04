from django.db import models
from authentication.models import User
from books.models import Book

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)