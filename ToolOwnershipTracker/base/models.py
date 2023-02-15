from django.db import models


# Create your models here.

class user(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=40, primary_key=True, Unique=True)
    role = models.IntegerField()  # radio buttons 1-3 for user type
    password = models.CharField(max_length=32)  # set to 32 for size of MD5 Hash
