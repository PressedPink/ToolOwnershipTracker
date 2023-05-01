from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User, UserType, Toolbox, Tool
from django.http import HttpResponseBadRequest
from django.http import request, JsonResponse
from django.shortcuts import render, get_object_or_404
from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Jobsite import JobsiteClass
from ToolOwnershipTracker.classes.Tool import ToolClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
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
        # currentEmail = request.session["username"]
        # currentUser = User.objects.get(email=currentEmail)
        # currentRole = currentUser.role
        return render(request, "signup.html")  # , {'role': currentRole})

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
        # currentEmail = request.session["username"]
        # currentUser = User.objects.get(email=currentEmail)
        # currentRole = currentUser.role
        try:
            UserClass.createUser(self, firstName, lastName, email, password, confirmPassword, address, phone, role)
            return render(request, "signup.html",
                          {"success_message": "User successfully created!"})  # , 'role': currentRole})
        except Exception as e:
            return render(request, "signup.html", {'error_message': str(e)})  # , 'role': currentRole})


class EditUser(View):
    def get(self, request):
        return render(request, "edituser.html")

    def post(self, request):
        email = request.session["username"]
        user = User.objects.get(email=email)
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
                return render(request, "edituser.html",
                              {'error_message': "Cannot update password without confirm password field!"})

        return redirect("/profile/")


class Profile(View):
    def get(self, request):

        # if helpers.redirectIfNotLoggedIn(request):
        #     return redirect("/")

        a = request.session["username"]
        b = User.objects.get(email=a)
        allSites = Jobsite.objects.all()
        assignedSites = []
        for site in allSites:
            if JobsiteClass.containsUser(self, site.id, b.email):
                assignedSites.append(site.id)

        return render(request, "profile.html", {"currentUser": b, "assignedSites": assignedSites})


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
            return render(request, 'ForgotPasswordTemplates/password_reset_form.html',
                          {'error_message': str(e), 'token': token})

        return render(request, 'ForgotPasswordTemplates/password_reset_form.html',
                      {'error_message': 'Failed to reset password.', 'token': token})


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
            if email_list:
                for email in email_list:
                    if len(email) != 0:
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
            assignedUsers = jobsite.assigned.all()
        except Exception as e:
            return render(request, 'createJobsites.html', {'error_message': str(e)})

        return render(request, 'editJobsite.html',
                      {'jobsite': jobsite, 'users': allUserEmails, 'assingedUsers': assignedUsers})

    def post(self, request, jobsite_id):
        title = request.POST.get('title')
        email = request.POST.get('owner')
        try:
            if (len(title) != 0):
                JobsiteClass.assignTitle(self, jobsite_id, title)
            if (len(email) != 0):
                JobsiteClass.assignOwner(self, jobsite_id, email)
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
            allJobsites = Jobsite.objects.all()
            return render(request, "jobsites.html", {'jobsites': allJobsites})
        except Exception as e:
            allUsers = User.objects.all()
            allUserEmails = [user.email for user in allUsers]
            jobsite = Jobsite.objects.get(id=jobsite_id)
            return render(request, 'editJobsite.html',
                          {'jobsite': jobsite, 'users': allUserEmails, 'error_message': str(e)})


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


class createTool(View):
    def get(self, request):
        jobsites = Jobsite.objects.all()
        allJobsiteNames = [jobsite.title for jobsite in jobsites]
        allUsers = User.objects.all()
        allUserEmails = [user.email for user in allUsers]

        allJobsiteNames = [jobsite.title for jobsite in jobsites]
        return render(request, 'createTool.html', {'users': allUserEmails, 'jobsites': allJobsiteNames})

    def post(self, request):
        name = request.POST.get('name')
        owner = request.POST.get('toolboxOwner')
        jobsiteName = request.POST.get('jobsiteName')
        toolbox_type = request.POST.get('toolboxType')
        tool_type = request.POST.get('toolType')
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
                        jobsite = Jobsite.objects.get(title=jobsiteName)
                        toolbox = Toolbox.objects.get(jobsite=jobsite)
                        ToolClass.addToToolbox(self, tool.id, toolbox.id)
                        return render(request, 'createTool.html')
                    except Exception as e:
                        return render(request, 'createTool.html', {'errror_message': str(e)})
                else:
                    return render(request, 'createTool.html',
                                  {'error_message': 'Please input a valid jobsite to assign tool to!'})
            else:
                return render(request, 'createTool.html',
                              {'error_message': 'Please input a jobsite to assign tool to!'})
        elif (toolbox_type == "UserToolbox"):
            if (len(owner) != 0):
                test = list(map(str, User.objects.filter(email=owner)))
                if len(test) != 0:
                    try:
                        ToolClass.createTool(self, name, type)
                        tool = Tool.objects.get(name=name)
                        toolbox = Toolbox.objects.get(owner=owner, jobsite=None)
                        ToolClass.addToToolbox(self, tool.id, toolbox.id)
                        return render(request, 'createTool.html')
                    except Exception as e:
                        return render(request, 'createTool.html', {'errror_message': str(e)})
                else:
                    return render(request, 'createTool.html',
                                  {'error_message': 'Please input a valid user to assign tool to'})
            else:
                return render(request, 'createTool.html', {'error_message': 'Please input an owner to assign tool to!'})
        else:
            try:
                ToolClass.createTool(self, name, type)
                return render(request, 'createTool.html')
            except Exception as e:
                return render(request, 'createTool.html', {'errror_message': str(e)})


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
        return render(request, "userToolboxes.html", {'users': allUsers, 'currentUser': user, 'sites': listOfSites})


class viewToolbox(View):
    def get(self, request, user_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        user = User.objects.get(email=user_id)  # user retrieved from user display page
        try:
            toolbox = Toolbox.objects.get(owner=user, jobsite=None)  # ask alex about jobsite=None !!!!
            toolsInBox = []
            tools = Tool.objects.all()
            for i in tools:
                if (i.toolbox == toolbox):
                    toolsInBox.append(i)
        except Exception as e:
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
                                                          'currentUser': user, 'sites': listOfSites})

        return render(request, 'userToolsAsUser.html', {"user": user, "tools": toolsInBox})


class myToolbox(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        a = request.session["username"]
        user = User.objects.get(email=a)
        userRole = user.role
        # add condition that prevents admins from seeing their toolbox cuz it doesn't exist
        toolbox = Toolbox.objects.get(owner=user, jobsite=None)  # ask alex about jobsite=None !!!!
        toolsInBox = []
        tools = Tool.objects.all()
        for i in tools:
            if i.toolbox == toolbox:
                toolsInBox.append(i)

        return render(request, 'currentUserToolbox.html', {"user": user, "tools": toolsInBox})


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

        return render(request, 'jobsiteToolboxes.html', {"sites": allJobsites})


class jobsiteInventory(View):
    def get(self, request, jobsite_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        try:
            jobsite = Jobsite.objects.get(id=jobsite_id)
            toolbox = Toolbox.objects.get(jobsite=jobsite)
            toolsInBox = []
            tools = Tool.objects.all()
            for i in tools:
                if i.toolbox == toolbox:
                    toolsInBox.append(i)

        except Exception as e:
            a = request.session["username"]
            user = User.objects.get(email=a)
            userRole = user.role
            if userRole == "A":
                allJobsites = Jobsite.objects.all()
            elif userRole == "S":
                allJobsites = Jobsite.objects.filter(owner=user)

            return render(request, 'jobsiteToolboxes.html', {'error_message': str(e), "sites": allJobsites})

        return render(request, 'jobsiteInventory.html', {"site": jobsite, "tools": toolsInBox})


class unassignedTools(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        allTools = Tool.objects.all()
        tools = []
        for tool in allTools:
            if tool.toolbox is None:
                tools.append(tool)

        return render(request, 'unassignedTools.html', {"tools": tools})


class editTool(View):
    def get(self, request, tool_id):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")
        tool = Tool.objects.get(id=tool_id)
        return render(request, 'editTool.html', {"tool": tool})
