import logging
import json
from PIL import Image
import io
import base64
from django.views import View
from .models import User, Jobsite, Toolbox, Tool, ToolReport
from ToolOwnershipTracker.classes.Jobsite import JobsiteClass
from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Tool import ToolClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.classes.ToolReport import ToolReportClass
from django.shortcuts import render, get_object_or_404, redirect
from pyzbar.pyzbar import decode
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, request
from django.db import connections
from datetime import datetime


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
        currentEmail = request.session["username"]
        currentUser = User.objects.get(email=currentEmail)
        currentRole = currentUser.role
        return render(request, "signup.html", {'role': currentRole})

    def post(self, request):

        # NEED TO MAKE SURE PASSWORD IS UTF-8
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        address = request.POST.get('address')
        phone = str(request.POST.get('phone'))
        role = request.POST.get('userTypeDropdown')
        currentEmail = request.session["username"]
        currentUser = User.objects.get(email=currentEmail)
        currentRole = currentUser.role
        try:
            UserClass.createUser(self, firstName, lastName, email, password, confirmPassword, address, phone, role)
            return render(request, "signup.html",
                          {'success_message': "User successfully created!", 'role': currentRole})
        except Exception as e:
            return render(request, "signup.html", {'error_message': str(e), 'role': currentRole})


class EditUser(View):
    def get(self, request):
        email = request.session["username"]
        user = User.objects.get(email=email)
        role = user.role
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]
        return render(request, "editUser.html", {'role': role, 'users': allUserEmails})

    def post(self, request):

        # From Session

        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]

        email = request.session["username"]
        user = User.objects.get(email=email)
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        role = request.POST.get('userTypeDropdown')
        userToEditEmail = request.POST.get('userEmail')
        if userToEditEmail:
            userToEdit = User.objects.get(email=userToEditEmail)
            userToEdit.role = role
            userToEdit.save()
            if len(phone) != 0:
                UserClass.editPhone(userToEdit, phone)
            if len(address) != 0:
                UserClass.editAddress(userToEdit, address)
            if len(newPassword) != 0:
                if len(confirmPassword) != 0:
                    try:
                        UserClass.change_password(userToEditEmail, newPassword, confirmPassword)
                    except Exception as e:
                        return render(request, "editUser.html",
                                      {'role': currentUserRole, 'users': allUserEmails, 'error_message': str(e)})
                else:
                    return render(request, "editUser.html",
                                  {'role': currentUserRole, 'users': allUserEmails,
                                   'error_message': "Cannot update password without confirm password field!"})
            return render(request, "editUser.html", {'role': currentUserRole, 'users': allUserEmails,
                                                     'success_message': "User information successfully edited!"})

        else:
            if len(phone) != 0:
                UserClass.editPhone(user, phone)
            if len(address) != 0:
                UserClass.editAddress(user, address)
            if len(newPassword) != 0:
                if len(confirmPassword) != 0:
                    try:
                        UserClass.change_password(email, newPassword, confirmPassword)
                    except Exception as e:
                        return render(request, "editUser.html",
                                      {'role': currentUserRole, 'users': allUserEmails, 'error_message': str(e)})
                else:
                    return render(request, "editUser.html",
                                  {'role': currentUserRole, 'users': allUserEmails,
                                   'error_message': "Cannot update password without confirm password field!"})
            return redirect("/profile/")


class Profile(View):
    def get(self, request):
        # if helpers.redirectIfNotLoggedIn(request):
        #     return redirect("/")

        a = request.session["username"]
        b = User.objects.get(email=a)
        role = b.role
        allSites = Jobsite.objects.all()
        assignedSites = []
        if b.role == "U":
            for site in allSites:
                if JobsiteClass.containsUser(self, site.id, b.email):
                    assignedSites.append(site.id)
        elif b.role == "S":
            for site in allSites:
                if site.owner == b:
                    assignedSites.append(site.id)

        return render(request, "profile.html", {"currentUser": b, "assignedSites": assignedSites, 'role': role})


class Login(View):
    def get(self, request):
        return render(request, "login.html")

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
            return render(request, "login.html", {"error_message": "No such user exists!"})

        elif badPassword:
            return render(request, "login.html", {"error_message": "Incorrect password!"})
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


@csrf_exempt
def process_image_to_tool(request):
    if request.method == 'POST':
        # Decode the base64 image data
        image_data = base64.b64decode(request.POST.get('image'))

        # Convert the image data to a PIL Image
        image = Image.open(io.BytesIO(image_data))

        # Process the image using Pyzbar
        decoded_objects = decode(image)
        results = []
        toolID = ""
        for obj in decoded_objects:
            if (obj.data.decode("utf-8")):
                toolID = obj.data.decode("utf-8")
                # Return the results as a JSON response
        response_data = {"toolID": toolID}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class barCodeTest(View):
    def get(self, request):
        return render(request, "barcodeTest.html")


class Jobsites(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role
        allJobsites = Jobsite.objects.all()
        return render(request, "jobsites.html", {'jobsites': allJobsites, 'role': currentUserRole})


class createJobsite(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allJobsites = Jobsite.objects.all()
        allUsers = User.objects.all()
        possibleOwnersEmails = []
        for user in allUsers:
            if user.role == "S":
                possibleOwnersEmails.append(user.email)
        allUserEmails = [user.email for user in allUsers]
        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role
        return render(request, 'createJobsites.html',
                      {'jobsites': allJobsites, 'users': allUserEmails, 'owners': possibleOwnersEmails,
                       'role': currentUserRole})

    def post(self, request):
        title = request.POST.get('title')
        owner = request.POST.get('owner')
        try:
            JobsiteClass.createJobsite(self, title, owner)
            jobsite = Jobsite.objects.get(owner=owner, title=title)
            allJobsites = Jobsite.objects.all()
            email_list = request.POST.get('email_list', '').split(',')
            if email_list:
                for email in email_list:
                    if len(email) != 0:
                        JobsiteClass.addUser(self, jobsite.id, email)
            allUsers = User.objects.all()
            possibleOwnersEmails = []
            for user in allUsers:
                if user.role == "S":
                    possibleOwnersEmails.append(user.email)
            allUserEmails = [user.email for user in allUsers]
            currentUserEmail = request.session["username"]
            currentUser = User.objects.get(email=currentUserEmail)
            currentUserRole = currentUser.role
            return render(request, 'createJobsites.html',
                          {'jobsites': allJobsites, 'users': allUserEmails, 'owners': possibleOwnersEmails,
                           'success_message': "Jobsite successfully created!", 'role': currentUserRole})
        except Exception as e:
            allJobsites = Jobsite.objects.all()
            allUsers = User.objects.all()
            possibleOwnersEmails = []
            for user in allUsers:
                if user.role == "S":
                    possibleOwnersEmails.append(user.email)
            allUserEmails = [user.email for user in allUsers]
            currentUserEmail = request.session["username"]
            currentUser = User.objects.get(email=currentUserEmail)
            currentUserRole = currentUser.role
            return render(request, 'createJobsites.html',
                          {'jobsites': allJobsites, 'users': allUserEmails, 'owners': possibleOwnersEmails,
                           'error_message': str(e), 'role': currentUserRole})


class editJobsite(View):
    def get(self, request, jobsite_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role

        try:
            jobsite = Jobsite.objects.get(id=jobsite_id)
            allUsers = User.objects.all()
            allUserEmails = [user.email for user in allUsers]
            assignedUsers = jobsite.assigned.all()
            possibleOwnersEmails = []
            for user in allUsers:
                if user.role == "S":
                    possibleOwnersEmails.append(user.email)
        except Exception as e:
            return render(request, 'editJobsite.html', {'error_message': str(e), 'role': currentUserRole})
        
        return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails, 'assingedUsers': assignedUsers, 'owners': possibleOwnersEmails, 'role': currentUserRole})
    def post(self, request, jobsite_id):
        title = request.POST.get('title')
        email = request.POST.get('owner')
        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role
        if 'deleteJobsite' in request.POST:
            try:
                JobsiteClass.removeJobsite(self, jobsite_id)
                return redirect("/jobsites/")
            except Exception as e:
                allUsers = User.objects.all()
                allUserEmails = [user.email for user in allUsers]
                jobsite = Jobsite.objects.get(id = jobsite_id)
                possibleOwnersEmails = []
                for user in allUsers:
                    if user.role == "S":
                        possibleOwnersEmails.append(user.email)
                return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails, 'owners': possibleOwnersEmails, 'error_message': str(e), 'role': currentUserRole})
        else:
            try:
                if (len(title) != 0):
                    JobsiteClass.assignTitle(self, jobsite_id, title)
                if (len(email) != 0):
                    JobsiteClass.assignOwner(self, jobsite_id, email)
                    jobsite = Jobsite.objects.get(id = jobsite_id)
                    toolbox = Toolbox.objects.get(jobsite = jobsite)
                    owner = User.objects.get(email = email)
                    toolbox.owner = owner
                    toolbox.save()
                email_list = request.POST.get('email_list', '').split(',')
                remove_email_list = request.POST.get('remove_email_list', '').split(',')
                if email_list:
                    for email in email_list:
                        if len(email) != 0:
                            JobsiteClass.addUser(self, jobsite_id, email)

                if remove_email_list:
                    for email in remove_email_list:
                        if len(email) != 0:
                            JobsiteClass.removeUser(self, jobsite_id, email)
                return redirect("/jobsites/")
            except Exception as e:
                allUsers = User.objects.all()
                allUserEmails = [user.email for user in allUsers]
                jobsite = Jobsite.objects.get(id = jobsite_id)
                possibleOwnersEmails = []
                for user in allUsers:
                    if user.role == "S":
                        possibleOwnersEmails.append(user.email)
                return render(request, 'editJobsite.html', {'jobsite': jobsite, 'users': allUserEmails, 'owners': possibleOwnersEmails, 'error_message': str(e), 'role': currentUserRole})


class createTool(View):
    def get(self, request):
        jobsites = Jobsite.objects.all()
        allJobsiteNames = [jobsite.title for jobsite in jobsites]
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]
        allJobsiteNames = [jobsite.title for jobsite in jobsites]
        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role
        return render(request, 'createTool.html',
                      {'users': allUserEmails, 'jobsites': allJobsiteNames, 'role': currentUserRole})

    def post(self, request):
        name = request.POST.get('name')
        owner = request.POST.get('toolboxOwner')
        jobsiteName = request.POST.get('jobsiteName')
        toolbox_type = request.POST.get('toolboxType')
        tool_type = request.POST.get('toolType')

        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role

        if (tool_type == "Handtool"):
            type = "H"
        if (tool_type == "Powertool"):
            type = "P"
        if (tool_type == "Operatable"):
            type = "D"
        if (tool_type == "Other"):
            type = "O"

        if (toolbox_type == "JobsiteToolbox"):
            if (len(jobsiteName) != 0):
                test = list(map(str, Jobsite.objects.filter(title=jobsiteName)))
                if len(test) != 0:
                    try:
                        ToolClass.createTool(self, name, type)
                        tool = Tool.objects.get(name=name)
                        tool.prevToolbox = None
                        jobsite = Jobsite.objects.get(title=jobsiteName)
                        toolbox = Toolbox.objects.get(jobsite=jobsite)
                        ToolClass.addToToolbox(self, tool.id, toolbox.id)
                        jobsites = Jobsite.objects.all()
                        allJobsiteNames = [jobsite.title for jobsite in jobsites]
                        allUsers = User.objects.all()
                        allUserEmails = [user.email for user in allUsers]

                        allJobsiteNames = [jobsite.title for jobsite in jobsites]
                        return render(request, 'createTool.html', {'users': allUserEmails, 'jobsites': allJobsiteNames,
                                                                   'success_message': "Tool successfully created!",
                                                                   'role': currentUserRole})

                    except Exception as e:
                        return render(request, 'createTool.html', {'error_message': str(e), 'role': currentUserRole})
                else:
                    return render(request, 'createTool.html',
                                  {'error_message': 'Please input a valid jobsite to assign tool to!',
                                   'role': currentUserRole})
            else:
                return render(request, 'createTool.html',
                              {'error_message': 'Please input a jobsite to assign tool to!', 'role': currentUserRole})
        elif (toolbox_type == "UserToolbox"):
            if (len(owner) != 0):
                test = list(map(str, User.objects.filter(email=owner)))
                if len(test) != 0:
                    try:
                        ToolClass.createTool(self, name, type)
                        tool = Tool.objects.get(name=name)
                        tool.checkout_datetime = datetime.now()
                        tool.save()
                        tool.prevToolbox = None
                        toolbox = Toolbox.objects.get(owner=owner, jobsite=None)
                        ToolClass.addToToolbox(self, tool.id, toolbox.id)
                        jobsites = Jobsite.objects.all()
                        allJobsiteNames = [jobsite.title for jobsite in jobsites]
                        allUsers = User.objects.all()
                        allUserEmails = [user.email for user in allUsers]

                        allJobsiteNames = [jobsite.title for jobsite in jobsites]
                        return render(request, 'createTool.html', {'users': allUserEmails, 'jobsites': allJobsiteNames,
                                                                   'success_message': "Tool successfully created!",
                                                                   'role': currentUserRole})

                    except Exception as e:
                        return render(request, 'createTool.html', {'error_message': str(e), 'role': currentUserRole})
                else:
                    return render(request, 'createTool.html',
                                  {'error_message': 'Please input a valid user to assign tool to',
                                   'role': currentUserRole})
            else:
                return render(request, 'createTool.html',
                              {'error_message': 'Please input an owner to assign tool to!', 'role': currentUserRole})
        else:
            try:
                ToolClass.createTool(self, name, type)
                jobsites = Jobsite.objects.all()
                allJobsiteNames = [jobsite.title for jobsite in jobsites]
                allUsers = User.objects.all()
                allUserEmails = [user.email for user in allUsers]
                allJobsiteNames = [jobsite.title for jobsite in jobsites]
                return render(request, 'createTool.html', {'users': allUserEmails, 'jobsites': allJobsiteNames,
                                                           'success_message': "Tool successfully created!",
                                                           'role': currentUserRole})

            except Exception as e:
                return render(request, 'createTool.html', {'error_message': str(e), 'role': currentUserRole})


class UserToolboxes(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        if userRole == 'S':  # only show users at supervisor's jobsites
            listOfSites = Jobsite.objects.filter(owner=user)  # filter out the jobsites that are owned by the user
            all = User.objects.all()
            allU = []
            for site in listOfSites:
                for i in all:
                    if JobsiteClass.containsUser(self, site.id, i.email):
                        allU.append(i)
            allUsers = {}
            for person in allU:
                assignedSites = ""
                added = False
                for site in listOfSites:
                    if JobsiteClass.containsUser(self, site.id, person.email):
                        if added:
                            assignedSites = assignedSites + ", " + str(site.id)
                        else:
                            assignedSites = str(site.id)
                        added = True
                allUsers.update({person: assignedSites})
        elif userRole == 'A':  # show all users
            allU = User.objects.all()
            allUsers = {}
            allSites = Jobsite.objects.all()
            for person in allU:
                if person.role == "U":
                    assignedSites = ""
                    added = False
                    for site in allSites:
                        if JobsiteClass.containsUser(self, site.id, person.email):
                            if added:
                                assignedSites = assignedSites + ", " + str(site.id)
                            else:
                                assignedSites = str(site.id)
                            added = True
                    if not added:
                        assignedSites = "Not Assigned"
                    allUsers.update({person: assignedSites})
                elif person.role == "S":
                    ownedSites = ""
                    added = False
                    for site in allSites:
                        if site.owner == person:
                            if added:
                                ownedSites = ownedSites + ", " + str(site.id)
                            else:
                                ownedSites = str(site.id)
                            added = True
                    if not added:
                        ownedSites = "Not Assigned"
                    allUsers.update({person: ownedSites})
        if user.role == "A":
            listOfSites = ""
            added = False
            allSites = Jobsite.objects.all()
            for site in allSites:
                if site.owner == user:
                    if added:
                        listOfSites = listOfSites + ", " + str(site.id)
                    else:
                        listOfSites = str(site.id)
                    added = True
            if not added:
                listOfSites = "None"
        elif user.role == "S":
            newListOfSites = ""
            listOfSites = Jobsite.objects.filter(owner=user)
            added = False
            for site in listOfSites:
                if added:
                    newListOfSites = newListOfSites + ", " + str(site.id)
                else:
                    newListOfSites = str(site.id)
                added = True
            if not added:
                newListOfSites = "None"
            listOfSites = newListOfSites
        return render(request, "userToolboxes.html",
                      {'users': allUsers, 'currentUser': user, 'sites': listOfSites, 'role': userRole})


class viewToolbox(View):
    def get(self, request, user_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        user = User.objects.get(email=user_id)  # user retrieved from user display page
        userRole = user.role

        AllJobsites = Jobsite.objects.all()
        allJobsiteTitles = [jobsite.title for jobsite in AllJobsites]

        try:
            toolbox = Toolbox.objects.get(owner=user, jobsite=None)  # ask alex about jobsite=None !!!!
            toolsInBox = []
            tools = Tool.objects.all()
            for i in tools:
                if (i.toolbox == toolbox):
                    toolsInBox.append(i)
        except Exception as e:
            if userRole == 'S':  # only show users at supervisor's jobsites
                listOfSites = Jobsite.objects.filter(owner=user)  # filter out the jobsites that are owned by the user
                all = User.objects.all()
                allU = []
                for site in listOfSites:
                    for i in all:
                        if JobsiteClass.containsUser(self, site.id, i.email):
                            allU.append(i)
                allUsers = {}
                for person in allU:
                    assignedSites = ""
                    added = False
                    for site in listOfSites:
                        if JobsiteClass.containsUser(self, site.id, person.email):
                            if added:
                                assignedSites = assignedSites + ", " + str(site.id)
                            else:
                                assignedSites = str(site.id)
                            added = True
                    allUsers.update({person: assignedSites})
            elif userRole == 'A':  # show all users
                allU = User.objects.all()
                allUsers = {}
                allSites = Jobsite.objects.all()
                for person in allU:
                    if person.role == "U":
                        assignedSites = ""
                        added = False
                        for site in allSites:
                            if JobsiteClass.containsUser(self, site.id, person.email):
                                if added:
                                    assignedSites = assignedSites + ", " + str(site.id)
                                else:
                                    assignedSites = str(site.id)
                                added = True
                        if not added:
                            assignedSites = "Not Assigned"
                        allUsers.update({person: assignedSites})
                    elif person.role == "S":
                        ownedSites = ""
                        added = False
                        for site in allSites:
                            if site.owner == person:
                                if added:
                                    ownedSites = ownedSites + ", " + str(site.id)
                                else:
                                    ownedSites = str(site.id)
                                added = True
                        if not added:
                            ownedSites = "Not Assigned"
                        allUsers.update({person: ownedSites})
            if user.role == "A":
                listOfSites = ""
                added = False
                allSites = Jobsite.objects.all()
                for site in allSites:
                    if site.owner == user:
                        if added:
                            listOfSites = listOfSites + ", " + str(site.id)
                        else:
                            listOfSites = str(site.id)
                        added = True
                if not added:
                    listOfSites = "None"
            elif user.role == "S":
                newListOfSites = ""
                listOfSites = Jobsite.objects.filter(owner=user)
                added = False
                for site in listOfSites:
                    if added:
                        newListOfSites = newListOfSites + ", " + str(site.id)
                    else:
                        newListOfSites = str(site.id)
                    added = True
                if not added:
                    newListOfSites = "None"
                listOfSites = newListOfSites
            return render(request, 'userToolboxes.html', {'error_message': str(e), "users": allUsers,
                                                          'currentUser': user, 'sites': listOfSites,
                                                          'role': currentUserRole})

        return render(request, 'userToolsAsAdmin.html', {"user": user, "tools": toolsInBox, 'role': currentUserRole})


class myToolbox(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]
        currentUserRole = user.role
        toolbox = Toolbox.objects.get(owner=user, jobsite=None)
        toolsInBox = []
        tools = Tool.objects.all()
        for i in tools:
            if i.toolbox == toolbox:
                toolsInBox.append(i)

        return render(request, 'currentUserToolbox.html',
                      {"user": user, "tools": toolsInBox, 'role': currentUserRole, 'users': allUserEmails})

    def post(self, request):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]

        if 'return' in request.POST:
            checked_tools = request.POST.getlist('tools')
            if len(checked_tools) != 0:
                for toolID in checked_tools:
                    currentTool = Tool.objects.get(id=toolID)
                    if currentTool.prevToolbox == None:
                        currentTool.toolbox = None
                        currentTool.save()
                    else:
                        currentTool.toolbox = currentTool.prevToolbox
                        currentTool.prevToolbox = None
                        currentTool.save()
                toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                toolsInBox = []
                tools = Tool.objects.all()
                for tool in tools:
                    if tool.toolbox == toolbox:
                        toolsInBox.append(tool)
                return render(request, 'currentUserToolbox.html',
                              {"user": user, "tools": toolsInBox, 'role': currentUserRole, 'users': allUserEmails})
            else:
                toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                toolsInBox = []
                tools = Tool.objects.all()
                for tool in tools:
                    if tool.toolbox == toolbox:
                        toolsInBox.append(tool)
                return render(request, 'currentUserToolbox.html',
                              {"user": user, "tools": toolsInBox, 'role': currentUserRole, 'users': allUserEmails,
                               'error_message': "Please select tool(s) to return!"})
        if 'sendTrade' in request.POST:
            checked_tools = request.POST.getlist('tools')
            userToTrade = request.POST.get('userToTrade')
            if len(checked_tools) != 0:
                if len(userToTrade) != 0:
                    if User.objects.filter(email=userToTrade).exists():
                        for toolID in checked_tools:
                            currentTool = Tool.objects.get(id=toolID)
                        toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                        toolsInBox = []
                        tools = Tool.objects.all()
                        for tool in tools:
                            if tool.toolbox == toolbox:
                                toolsInBox.append(tool)
                        return render(request, 'currentUserToolbox.html',
                                      {"user": user, "tools": toolsInBox, 'role': currentUserRole,
                                       'users': allUserEmails})
                    else:
                        toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                        toolsInBox = []
                        tools = Tool.objects.all()
                        for tool in tools:
                            if tool.toolbox == toolbox:
                                toolsInBox.append(tool)
                        return render(request, 'currentUserToolbox.html',
                                      {"user": user, "tools": toolsInBox, 'role': currentUserRole,
                                       'users': allUserEmails,
                                       'error_message': "Please input a valid user to trade with!"})
                else:
                    toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                    toolsInBox = []
                    tools = Tool.objects.all()
                    for tool in tools:
                        if tool.toolbox == toolbox:
                            toolsInBox.append(tool)
                    return render(request, 'currentUserToolbox.html',
                                  {"user": user, "tools": toolsInBox, 'role': currentUserRole, 'users': allUserEmails,
                                   'error_message': "Please input a user to trade with!"})
            else:
                toolbox = Toolbox.objects.get(owner=user, jobsite=None)
                toolsInBox = []
                tools = Tool.objects.all()
                for tool in tools:
                    if tool.toolbox == toolbox:
                        toolsInBox.append(tool)
                return render(request, 'currentUserToolbox.html',
                              {"user": user, "tools": toolsInBox, 'role': currentUserRole, 'users': allUserEmails,
                               'error_message': "Please select tool(s) to trade!"})


class fileToolReport(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role

        toolbox = Toolbox.objects.get(owner=currentUser, jobsite=None)
        toolsInPersonalToolbox = []
        tools = Tool.objects.all()
        for tool in tools:
            if tool.toolbox == toolbox:
                toolsInPersonalToolbox.append(tool)

        allJobsites = Jobsite.objects.all()
        allTools = Tool.objects.all()
        jobsiteToolDictionary = {}
        for jobsite in allJobsites:
            if jobsite.owner == currentUser:
                currentSiteTools = []
                for tool in allTools:
                    if tool.toolbox != None:
                        if tool.toolbox.jobsite != None:
                            if tool.toolbox.jobsite == jobsite:
                                currentSiteTools.append(tool)
                jobsiteToolDictionary.update({jobsite: currentSiteTools})

        return render(request, 'toolReportForm.html', {'role': currentUserRole, 'tools': toolsInPersonalToolbox,
                                                       'jobsiteToolDictionary': jobsiteToolDictionary})

    def post(self, request):

        currentUserEmail = request.session["username"]
        currentUser = User.objects.get(email=currentUserEmail)
        currentUserRole = currentUser.role

        toolbox = Toolbox.objects.get(owner=currentUser, jobsite=None)
        toolsInBox = []
        tools = Tool.objects.all()
        for tool in tools:
            if tool.toolbox == toolbox:
                toolsInBox.append(tool)

        toolName = request.POST.get('toolDropdown')
        description = request.POST.get('description')
        reportType = request.POST.get('reportType')

        toolToReport = Tool.objects.get(name=toolName)
        toolID = toolToReport.id
        toolbox = toolToReport.toolbox
        toolboxID = toolbox.id
        jobsiteID = None

        if toolbox.jobsite is None:
            # user toolbox
            if toolToReport.prevToolbox is None:
                jobsiteID = None
            else:
                jobsiteID = toolToReport.prevToolbox.jobsite.id
        else:
            # jobsite toolbox
            jobsiteID = toolbox.jobsite.id

        try:
            ToolReportClass.createToolReport(self, currentUserEmail, toolID, toolboxID, reportType, description,
                                             jobsiteID)
            toolToReport.toolbox = None
            toolToReport.checkout_datetime = None
            toolToReport.save()
            allJobsites = Jobsite.objects.all()
            allTools = Tool.objects.all()
            jobsiteToolDictionary = {}
            for jobsite in allJobsites:
                if jobsite.owner == currentUser:
                    currentSiteTools = []
                    for tool in allTools:
                        if tool.toolbox != None:
                            if tool.toolbox.jobsite != None:
                                if tool.toolbox.jobsite == jobsite:
                                    currentSiteTools.append(tool)
                    jobsiteToolDictionary.update({jobsite: currentSiteTools})
            return render(request, 'toolReportForm.html', {'role': currentUserRole, 'tools': toolsInBox,
                                                           'success_message': "Tool report successfully created!",
                                                           'jobsiteToolDictionary': jobsiteToolDictionary})
        except Exception as e:
            allJobsites = Jobsite.objects.all()
            allTools = Tool.objects.all()
            jobsiteToolDictionary = {}
            for jobsite in allJobsites:
                if jobsite.owner == currentUser:
                    currentSiteTools = []
                    for tool in allTools:
                        if tool.toolbox != None:
                            if tool.toolbox.jobsite != None:
                                if tool.toolbox.jobsite == jobsite:
                                    currentSiteTools.append(tool)
                    jobsiteToolDictionary.update({jobsite: currentSiteTools})
            return render(request, 'toolReportForm.html',
                          {'role': currentUserRole, 'tools': toolsInBox, 'error_message': str(e),
                           'jobsiteToolDictionary': jobsiteToolDictionary})


class jobsiteToolboxes(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        if userRole == "A":
            allJobsites = Jobsite.objects.all()
        elif userRole == "S":
            allJobsites = Jobsite.objects.filter(owner=user)

        return render(request, 'jobsiteToolboxes.html', {"sites": allJobsites, 'role': userRole})


class jobsiteInventory(View):
    def get(self, request, jobsite_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        try:
            jobsite = Jobsite.objects.get(id=jobsite_id)
            toolbox = Toolbox.objects.get(jobsite=jobsite)
            toolsInBox = []
            tools = Tool.objects.all()
            for i in tools:
                if i.toolbox == toolbox:
                    toolsInBox.append(i)

        except Exception as e:

            if userRole == "A":
                allJobsites = Jobsite.objects.all()
            elif userRole == "S":
                allJobsites = Jobsite.objects.filter(owner=user)

            return render(request, 'jobsiteToolboxes.html',
                          {'error_message': str(e), "sites": allJobsites, 'role': userRole})

        return render(request, 'jobsiteInventory.html', {"site": jobsite, "tools": toolsInBox, 'role': userRole})


class ScanToUserToolbox(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        message = ""
        jobsiteList = Jobsite.objects.filter(assigned=a)

        return render(request, 'barcodeScanToUser.html',
                      {"user": user, "message": message, "jobsiteList": jobsiteList, 'role': userRole})

    def post(self, request):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        jobsiteList = Jobsite.objects.filter(assigned=a)

        message = ""
        toolID = "base"
        result = request.POST.get('result')
        siteSelection = request.POST.get('userSites').split('|')[0].strip()
        try:

            dict = json.loads(result)
            toolID = dict["toolID"]


        except:
            message = message + "bad barcode read"

        try:
            sysTool = Tool.objects.get(id=toolID)

        except:
            message = message + "tool does not exist in system"

        try:
            userToolbox = Toolbox.objects.get(
                owner=user, jobsite=siteSelection)
            if (ToolClass.containedInAnyToolbox(sysTool.id)):
                ToolClass.removeFromToolbox(self, sysTool.id, sysTool.toolbox.id)

            ToolClass.addToToolbox(self, sysTool.id, userToolbox.id)

        except:
            message = message + "tool was not moved properly"

        message = siteSelection

        return render(request, 'barcodeScanToUser.html',
                      {"user": user, "message": message, "jobsiteList": jobsiteList, 'role': currentUserRole})


class ScanToJobsiteToolbox(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role

        jobsiteList = Jobsite.objects.get(owner=user)
        toolsInBox = []
        message = ""

        return render(request, 'barcodeScanToJobsite.html',
                      {"user": user, "jobsites": jobsiteList, "message": message, 'role': userRole})

    def post(self, request):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        message = "error"

        return render(request, 'barcodeScanToUser.html', {"user": user, "message": message, 'role': currentUserRole})


class viewToolReports(View):
    def get(self, request):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        allReports = ToolReport.objects.all()
        return render(request, 'toolReports.html', {'role': currentUserRole, 'reports': allReports})

class toolReportDetails(View):
    def get(self, request, toolreport_id):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        toolReport = ToolReport.objects.get(id = toolreport_id)
        return render(request, 'individualToolReport.html', {'role': currentUserRole, 'report': toolReport})
    def post(self, request, toolreport_id):
        a = request.session["username"]
        user = User.objects.get(email=a)
        currentUserRole = user.role
        toolReport = ToolReport.objects.get(id = toolreport_id)
        toolReport.delete()
        allReports = ToolReport.objects.all()
        return render(request, 'toolReports.html', {'role': currentUserRole, 'reports': allReports})

class unassignedTools(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        allTools = Tool.objects.all()
        allReports = ToolReport.objects.all()
        ToolDict = {}

        for tool in allTools:
            if tool.toolbox is None:
                status = "None"
                for report in allReports:
                    if report.tool == tool:
                        status = str(report.reportType)
                ToolDict.update({tool: status})
        print("ToolDict = ")
        print(ToolDict)

        return render(request, 'unassignedTools.html', {"tools": ToolDict, "user": user, "role": userRole})


class editTool(View):
    def get(self, request, tool_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        tool = Tool.objects.get(id=tool_id)
        return render(request, 'editTool.html', {"tool": tool, "role": userRole})
