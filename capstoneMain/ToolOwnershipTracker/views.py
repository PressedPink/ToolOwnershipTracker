from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType
import uuid

from django.http import request, JsonResponse
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
        
class PasswordReset(View):
    def get(self, request):
        return render(request, "ForgotPasswordTemplates/password_reset.html")

    def post(self, request):
        tempEmail = request.POST.get('email')
        destination = UserClass.forget_password(tempEmail)
        if(destination):
            return redirect("/password_reset_sent/")
        else:
            return JsonResponse({"error": "This is an error"})

class PasswordResetSent(View):
    def get(self, request):
        return render(request, "/ForgotPasswordTemplates/password_reset_sent.html")

class PasswordResetForm(View):
    def get(self, request):
        return render(request, "ForgotPasswordTemplates/password_reset_form.html")
    
    def post(self, request):
        email = request.Post.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm-password')
        try:
            UserClass.change_password(email, password, confirmPassword)
            return redirect("/password_reset_done/")
        except Exception as e:
            return render(request, 'ForgotPasswordTemplates/password_reset_form.html', {'error_message':str(e)})
            


class PasswordResetDone(View):
    def get(self, request):
        return render(request, "/ForgotPasswordTemplates/password_reset_done.html")
    
    def post(self, request):
        return redirect("")
