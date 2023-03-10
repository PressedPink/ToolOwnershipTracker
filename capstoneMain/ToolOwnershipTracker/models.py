from django.db import models
from django.forms import ModelForm, forms

# defining three user roles for our app


class UserType(models.TextChoices):
    Supervisor = "S"
    Admin = "A"
    User = "U"

# defines the user model, which contains the following fields: username, password, accountType, email, address and phone number


class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=40, primary_key=True)
    role = models.CharField(
        max_length=1, choices=UserType.choices, default=UserType.User)
    # set to 32 for size of MD5 Hash
    password = models.CharField(max_length=32)
    address = models.CharField(max_length=300, default="")
    phone = models.CharField(max_length=14, default="")
