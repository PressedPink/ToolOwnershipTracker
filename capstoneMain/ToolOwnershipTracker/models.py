from django.db import models
from django.forms import ModelForm, forms
from django.contrib import admin


# defining three user roles for our app


class UserType(models.TextChoices):
    Supervisor = "S"
    Admin = "A"
    User = "U"


class ToolType(models.TextChoices):
    Handtool = "H"
    Powertool = "P"
    Operatable = "D"
    Other = "O"


class reportType(models.TextChoices):
    # Tool is damaged in some way
    Damaged = "D"
    # Tool has been lost
    Lost = "L"


# defines the user model, which contains the following fields: username, password, accountType, email, address,
# phone number and active status

# defines a User of any type
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
    # records if user is active for security purposes
    active = models.BooleanField
    forget_password_token = models.CharField(max_length=100, default="")


# defines a Jobsite
class Jobsite(models.Model):
    id = models.AutoField(primary_key=True)
    # dictates supervisor that can view
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=40, unique=True)
    # dictates users that can view
    assigned = models.ManyToManyField(User, related_name='assigned', blank=True)


class Toolbox(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, )
    jobsite = models.ForeignKey(Jobsite, on_delete=models.CASCADE, null=True)


class Tool(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)
    
    toolType = models.CharField(
        max_length=1, choices=ToolType.choices, default=ToolType.Other)
    toolbox = models.ForeignKey(Toolbox, on_delete=models.CASCADE, null=True)
    prevToolbox = models.ForeignKey(Toolbox, on_delete=models.CASCADE, related_name='prevToolbox', null=True)
    checkout_datetime = models.DateTimeField(blank=True, null=True)


class ToolReport(models.Model):
    id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    reportType = models.CharField(max_length=1, choices=reportType.choices, default=reportType.Damaged)
    tool = models.ForeignKey(Tool, null=False, on_delete=models.CASCADE)
    toolbox = models.ForeignKey(Toolbox, null=False, on_delete = models.CASCADE)
    jobsite = models.ForeignKey(Jobsite, null=True, on_delete = models.CASCADE)
    description = models.CharField(max_length=500)
