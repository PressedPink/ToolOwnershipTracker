from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType
import uuid

from django.http import request
from django.shortcuts import render
from ToolOwnershipTracker.classes.Users import UserClass
from . import models
from .models import User
from django.views import View
import logging

# Create your views here.


# class Login(View):
#    email = str(request.POST['Email Address']).strip()
#    password = str(request.POST['Password'])


# class SignUp(View):
#    firstName = str(request.POST['First Name'])
#    lastName = str(request.POST['Last Name'])
#    email = str(request.POST['Email Address']).strip()
#    password = str(request.POST['Password'])
#    confirmPassword = str(request.POST['Confirm Password'])
#    Role = str(request.P0ST['User Type'])
#    address = str(request.POST['Address'])
#    phoneNumber = str(request.POST['Phone Number'])


# For the signup.html page, which allows the user to be redirected to the signup page when successfully or unsuccesfully signing up.


class Profile(View):
    def get(self, request):
        a = request.session["email"]
        b = User.objects.get(email=a)

        return render(request, "profile.html", {"currentUser": b})


class Login(View):
    def get(self, request):
        return render(request, "LoginHTML.html")

    def post(self, request):

        return redirect("/profile/")
