from django.db import models


# Create your models here.

class user(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=40, primary_key=True, Unique=True)
    role = models.CharField(max_length=1, choices=UserType.choices, default=UserType.user)
    password = models.CharField(max_length=32)  # set to 32 for size of MD5 Hash
    address = models.CharField(max_length=300, default="")
    phone = models.CharField(max_length=14, default="")

    def __str__(self):
        return self.username
