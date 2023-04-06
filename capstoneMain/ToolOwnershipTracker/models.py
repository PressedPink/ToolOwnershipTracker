from django.db import models
from django.forms import ModelForm, forms

# defining three user roles for our app
from capstoneMain.ToolOwnershipTracker.classes import Tool
from capstoneMain.ToolOwnershipTracker.classes.Toolbox import Toolbox


class UserType(models.TextChoices):
    Supervisor = "S"
    Admin = "A"
    User = "U"


# defines the user model, which contains the following fields: username, password, accountType, email, address,
# phone number and active status


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
    active = models.BooleanField


class Jobsite(models.Model):
    id = models.ForeignKey(unique=True, primary_key=True)
    owner = models.CharField(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=40)
    assigned = models.CharField(User, on_delete=models.CASCADE, null=True)
    toolbox = models.CharField(Toolbox, on_delete=models.CASCADE, null=False)


class Toolbox(models.Model):
    id = models.ForeignKey(unique=True, primary_key=True)
    tools = models.CharField(Tool, on_delete=models.CASCADE, null=True)
    owner = models.CharField(User, on_delete=models.CASCADE, null=False)


class Tool(models.Model):
    id = models.ForeignKey(unique=True, primary_key=True)
    jobsite = models.CharField(Jobsite, on_delete=models.CASCADE, null=True)
    user = models.CharField(User, on_delete=models.CASCADE, null=True)
