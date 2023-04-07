import logging
from django.views import View
from .models import User, Jobsite
from .classes.Jobsite import JobsiteClass
from . import models
from django.shortcuts import render
from ToolOwnershipTracker.classes.Jobsite import JobsiteClass
from ToolOwnershipTracker.classes.Users import UserClass
from django.shortcuts import render, get_object_or_404
from pyzbar.pyzbar import decode
from PIL import Image
import io
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType
from django.http import HttpResponseBadRequest
from django.http import request, JsonResponse


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
        firstName = str(request.POST['firstName'])
        lastName = str(request.POST['lastName'])
        email = str(request.POST['email']).strip()
        password = str(request.POST['password1'])
        confirmPassword = str(request.POST['password2'])
        # Role = str(request.P0ST['User Type'])
        address = str(request.POST['address'])
        phoneNumber = str(request.POST['phone'])

        UserClass.createUser(UserClass, email=email, password=password, firstName=firstName,
                             lastName=lastName, phone=phoneNumber, address=address, confirmPassword=confirmPassword)
        return redirect('/')


# For the signup.html page, which allows the user to be redirected to the signup page when successfully or unsuccesfully signing up.
class SignUp(View):
    def get(self, request):
        return render(request, "signup.html")


class EditUser(View):
    def get(self, request):
        return render(request, "edituser.html")


class Profile(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        a = request.session["username"]
        b = User.objects.get(email=a)

        return render(request, "profile.html", {"currentUser": b})


class Login(View):
    def get(self, request):
        # print(UserClass.hashPass("alexf"))
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

            print(password)
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
            return render(request, 'ForgotPasswordTemplates/password_reset_form.html',
                          {'error_message': str(e), 'token': token})

        return render(request, 'ForgotPasswordTemplates/password_reset_form.html',
                      {'error_message': 'Failed to reset password.', 'token': token})


class PasswordResetDone(View):
    def get(self, request):
        return render(request, 'ForgotPasswordTemplates/password_reset_done.html')

    def post(self, request):
        return redirect("")


class Jobsites(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allJobsites = Jobsite.objects.all()
        return render(request, "jobsites.html", {'jobsites': allJobsites})


class editUsers(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        return render(request, "edituser.html")


@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        # Decode the base64 image data
        image_data = base64.b64decode(request.POST.get('image'))

        # Convert the image data to a PIL Image
        image = Image.open(io.BytesIO(image_data))

        # Process the image using Pyzbar
        decoded_objects = decode(image)
        results = []
        for obj in decoded_objects:
            results.append({
                'type': obj.type,
                'data': obj.data.decode("utf-8")
            })

        # Return the results as a JSON response
        response_data = {'results': results}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class barCodeTest(View):
    def get(self, request):
        return render(request, "barcodeTest.html")


class createJobsite(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allJobsites = Jobsite.objects.all()
        return render(request, 'createJobsites.html', {'jobsites': allJobsites})

    def post(self, request):
        title = request.POST.get('title')
        owner = request.POST.get('owner')
        try:
            JobsiteClass.createJobsite(self, title, owner)
            allJobsites = Jobsite.objects.all()
            return render(request, 'createJobsites.html', {'jobsites': allJobsites})
        except Exception as e:
            return render(request, 'createJobsites.html', {'error_message': str(e)})


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
        owner = request.POST.get('owner')
        email_list = request.POST.getlist('email_list[]')
        jobsite = Jobsite.objects.get(id=jobsite_id)
        try:
            JobsiteClass.changeTitle(jobsite, title)
            JobsiteClass.assignOwner(jobsite, owner)
            allJobsites = Jobsite.objects.all()
            return render(request, "jobsites.html", {'jobsites': allJobsites})
        except Exception as e:
            allUsers = User.objects.all()
            allUserEmails = [user.email for user in allUsers]
            return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails, 'error_message': str(e)})

        return render(request, 'editJobsite.html')

    def post(self, request):
        title = request.POST.get('title')
        owner = request.POST.get('owner')


class UserToolboxes(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        if userRole == 'S':  # only show users at supervisor's jobsite
            listOfSites = Jobsite.objects.filter(
                owner=user)  # filter out the jobsites that are owned by the current user
            all = User.objects.all()
            allUsers = []
            for site in listOfSites:
                for i in all:
                    if site.containsUser(i):
                        allUsers.append(i)

        elif userRole == 'A':  # show all users
            allUsers = User.objects.all()

        # allUsers = User.objects.all()

        return render(request, "userToolboxes.html", {'users': allUsers})


class viewToolbox(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        return render(request, 'userToolsAsUser.html')
