from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime, now

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    query = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=50)
