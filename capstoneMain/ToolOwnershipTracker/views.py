from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType
from django.http import HttpResponseBadRequest
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
        a = request.session["username"]
        b = User.objects.get(email=a)

        return render(request, "profile.html", {"currentUser": b})

class Login(View):
    def get(self, request):
        return render(request, "LoginHTML.html")

    def post(self, request):

        if 'forgot_password' in request.POST:
            return redirect("/password_reset/")

        noSuchUser = False
        blankName = False
        badPassword = False

        try:
            email = request.POST['InputUsername']
            user = User.objects.get(email=email)
            password = request.POST['InputPassword']
            password = UserClass.hashPass(password)
            badPassword = (user.password != password)
        except Exception as e:
            noSuchUser = True

        if noSuchUser:
            return render(request, "LoginHTML.html", {"message": "no user"})

        elif badPassword:
            return render(request, "LoginHTML.html", {"message": "bad password"})
        else:
            request.session["username"] = user.email
            # request.session["name"] = user.name
            return redirect("/profile/")

        
class PasswordReset(View):
    def get(self, request):
        return render(request, "ForgotPasswordTemplates/password_reset.html")

    def post(self, request):
        tempEmail = request.POST.get('email')
        try:
            UserClass.forget_password(tempEmail)
            return redirect("/password_reset_sent/")
        except Exception as e:
            return render(request, 'ForgotPasswordTemplates/password_reset.html', {'error_message':str(e)})
            

class PasswordResetSent(View):
    def get(self, request):
        return render(request, 'ForgotPasswordTemplates/password_reset_sent.html')

class PasswordResetForm(View):
    def get(self, request, token):
        try:
            user = User.objects.get(forget_password_token = token)
            email = user.email
            if UserClass.check_reset_password_token(email, token):
                return render(request, 'ForgotPasswordTemplates/password_reset_form.html', {'token': token})
        except User.DoesNotExist:
            pass
        return HttpResponseBadRequest()
    
    def post(self, request, token):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        token = request.POST.get('token')
        
        try:
            if UserClass.change_password(email, password, confirm_password):
                return redirect("/password_reset_done/")
        except Exception as e:
            return render(request, 'ForgotPasswordTemplates/password_reset_form.html', {'error_message': str(e), 'token': token})
        
        return render(request, 'ForgotPasswordTemplates/password_reset_form.html', {'error_message': 'Failed to reset password.', 'token': token})

class PasswordResetDone(View):
    def get(self, request):
        return render(request, 'ForgotPasswordTemplates/password_reset_done.html')
    
    def post(self, request):
        return redirect("")