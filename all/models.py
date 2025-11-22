from django.db import models
from django.contrib.auth.hashers import make_password

class Profile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username