import uuid

from django.http import request
from django.shortcuts import render
from ToolOwnershipTracker.ToolOwnershipTracker.Users import User
from . import models
from .models import user
from django.views import View
import logging

# Create your views here.

class Login(View):
    email = str(request.POST['Email Address']).strip()
    password = str(request.POST['Password'])

class SignUp(View):
    firstName = str(request.POST['First Name'])
    lastName = str(request.POST['Last Name'])
    email = str(request.POST['Email Address']).strip()
    password = str(request.POST['Password'])
    confirmPassword = str(request.POST['Confirm Password'])
    Role = str(request.P0ST['User Type'])
    address = str(request.POST['Address'])
    phoneNumber = str(reques.POST['Phone Number'])


