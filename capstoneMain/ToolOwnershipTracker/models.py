from django.db import models
from django.forms import ModelForm, forms
from django.contrib import admin


# defining three user roles for our app


class UserType(models.TextChoices):
    Supervisor = "S"
    Admin = "A"
    User = "U"


class reportType(models.TextChoices):
    # insident occured but no noteable damage displayed at this time
    Report = "R"
    # Tool is damaged in some way
    Damaged = "D"
    # Injury to someone occurred
    Injury = "I"
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
    id = models.CharField(max_length=50, primary_key=True)
    # dictates supervisor that can view
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=40)
    # dictates users that can view
    assigned = models.CharField(User, null=True, max_length=50)


# defines a toolbox for a Jobsite OR a User -- should NOT have both
# noteownerANDjobsite should not BOTH be null, will verify and address in logic


class Toolbox(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=50, )
    tools = models.CharField(Tool, null=True, max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, )
    jobsite = models.ForeignKey(Jobsite, on_delete=models.CASCADE, null=True)


# defines a tool. Tools WITHOUT a toolbox are not assigned to a user OR a jobsite


class Tool(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=50)
    toolbox = models.ForeignKey(Toolbox, on_delete=models.CASCADE, null=True)


class ToolReport(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=50)
    reporter = models.CharField(user, null=False, max_length=50)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    # used if injury occurred
    impactedUsers = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tool = models.CharField(Tool, null=True)
    # reports the location at time of incident
    jobSite = models.CharField(Jobsite)
    # time incident occurred
    time = models.datetime(auto_now_add=True)
    reportType = models.CharField(max_length=1, choices=ReportType.choices, default=ReportType.Report)
    description = models.CharField(max_length=350)
