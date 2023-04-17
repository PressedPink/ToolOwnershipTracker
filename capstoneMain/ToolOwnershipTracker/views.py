from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType
from django.http import HttpResponseBadRequest
from django.http import request, JsonResponse
from django.shortcuts import render, get_object_or_404
from ToolOwnershipTracker.classes.Users import UserClass 
from ToolOwnershipTracker.classes.Jobsite import JobsiteClass
from . import models
from .models import User, Jobsite
from django.views import View
from django.db import connections
import logging
# Create your views here.


# class Login(View):
#    email = str(request.POST['Email Address']).strip()
#    password = str(request.POST['Password'])
class helpers():
    def redirectIfNotLoggedIn(request):
        if request.session["username"] is None:
            return True
        else:
            return False


class SignUp(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):

        # NEED TO MAKE SURE PASSWORD IS UTF-8
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        # Role = str(request.P0ST['User Type'])
        address = request.POST.get('address')
        phone = str(request.POST.get('phone'))
        try:
            UserClass.createUser(self, firstName, lastName, email, password, confirmPassword, address, phone)
            return redirect('/')
        except Exception as e:
            return render(request, "signup.html", {'error_message': str(e)})


class EditUser(View):
    def get(self, request):
        return render(request, "edituser.html")
    def post(self, request):
        email = request.session["username"]
        user = User.objects.get(email = email)
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        if len(phone) != 0:
            UserClass.editPhone(user, phone)
        if len(address) != 0:
            UserClass.editAddress(user, address)
        if len(newPassword) != 0:
            if len(confirmPassword) != 0:
                try:
                    UserClass.change_password(email, newPassword, confirmPassword)
                except Exception as e:
                    return render(request, "edituser.html", {'error_message': str(e)})
            else:
                return render(request, "edituser.html", {'error_message': "Cannot update password without confirm password field!"})


        return redirect("/profile/")
        

class Profile(View):
    def get(self, request):

       # if helpers.redirectIfNotLoggedIn(request):
       #     return redirect("/")

        a = request.session["username"]
        b = User.objects.get(email=a)
        return render(request, "profile.html", {"currentUser": b})


class Login(View):
    def get(self, request):
        #print(UserClass.hashPass("alexf"))
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
            return render(request, "LoginHTML.html", {"error_message": "No such user exists!"})

        elif badPassword:
            return render(request, "LoginHTML.html", {"error_message": "Incorrect password!"})
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
            print(e)
            return render(request, 'ForgotPasswordTemplates/password_reset.html', {'error_message': str(e)})


class PasswordResetSent(View):
    def get(self, request):

        return render(request, 'ForgotPasswordTemplates/password_reset_sent.html')


class PasswordResetForm(View):
    def get(self, request, token):
        try:
            user = User.objects.get(forget_password_token=token)
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

class editUsers(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        return render(request, "edituser.html")

class Jobsites(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allJobsites = Jobsite.objects.all()
        assigned_users = [list(jobsite.assigned.all()) for jobsite in allJobsites]
        return render(request, "jobsites.html", {'jobsites': allJobsites})

class createJobsite(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allJobsites = Jobsite.objects.all()
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]
        return render(request, 'createJobsites.html', {'jobsites': allJobsites, 'users': allUserEmails})
    def post(self, request):
        title = request.POST.get('title')
        owner = request.POST.get('owner')
        try:
            JobsiteClass.createJobsite(self, title, owner)
            jobsite = Jobsite.objects.get(owner=owner, title=title)
            allJobsites = Jobsite.objects.all()
            email_list = request.POST.get('email_list', '').split(',')
            for email in email_list:
                JobsiteClass.addUser(self, jobsite.id, email)
            return render(request, 'createJobsites.html', {'jobsites': allJobsites})
        except Exception as e:
            allJobsites = Jobsite.objects.all()
            return render(request, 'createJobsites.html', {'jobsites': allJobsites, 'error_message': str(e)})
        
class editJobsite(View):
    def get(self, request, jobsite_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        try:
            jobsite = Jobsite.objects.get(id=jobsite_id)
            allUsers = User.objects.all()
            allUserEmails = [user.email for user in allUsers]
        except Exception as e:
            return render(request, 'createJobsites.html', {'error_message': str(e)})
        
        return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails})
    def post(self, request, jobsite_id):
        title = request.POST.get('title')
        email = request.POST.get('owner')
        email_list = request.POST.getlist('emails[]')
        try:
            JobsiteClass.assignTitle(self, jobsite_id, title)
            JobsiteClass.assignOwner(self, jobsite_id, email)
            #for email in email_list:
                #JobsiteClass.addUser(self, jobsite_id, email)
                #jobsite = Jobsite.objects.get(id = jobsite_id)
            #allJobsites = Jobsite.objects.all()
            #assigned_users = [list(jobsite.assigned.all()) for jobsite in allJobsites]
            #for users in assigned_users:
                #for user in users:
                   # print(user.firstName)
            #print("HEllO")
            allJobsites = Jobsite.objects.all()
            return render(request, "jobsites.html", {'jobsites': allJobsites})
        except Exception as e:
            allUsers = User.objects.all()
            allUserEmails = [user.email for user in allUsers]
            jobsite = Jobsite.objects.get(id = jobsite_id)
            return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails, 'error_message': str(e)})
    
class removeJobsite(View):
    def post(self, request, jobsite_id):
        try:
            JobsiteClass.removeJobsite(self, jobsite_id)
        except Exception as e:
            allJobsites = Jobsite.objects.all()
            redirect("/jobsites/")
            return render(request, "jobsites.html", {'error_message': str(e), 'jobsites': allJobsites})
        allJobsites = Jobsite.objects.all()
        return redirect("/jobsites/")
