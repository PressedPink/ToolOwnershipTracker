from django.shortcuts import render, redirect
# from classes.profile import Profile
from ToolOwnershipTracker.models import User
from django.http import HttpResponseBadRequest
from ToolOwnershipTracker.classes.Users import UserClass
from .models import User, Jobsite, Toolbox, Tool, ToolReport
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from ToolOwnershipTracker.forms import ReportForm
# Create your views here.

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
        print(UserClass.hashPass("alexf"))
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


class Jobsites(View):
    def get(self, request):
        #if helpers.redirectIfNotLoggedIn(request):
            #return redirect("/")
        allJobsites = Jobsite.objects.all()
        return render(request, "jobsites.html", {'jobsites': allJobsites})


class editUsers(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
            return redirect("/")

        return render(request, "edituser.html")

class viewJobsitesSuperAdmin(View):
    def get(self, request):
        jobsites = Jobsite.objects.all()
        user = request.session["email"]
        accType = request.session["role"]
        toolbox = Toolbox.objects.all()
        return render(request, "jobsiteToolsAsSA.html", {'jobsites': jobsites, 'accType': accType, 'user': user, 'toolbox' : toolbox})

class ReportListView(ListView):
    model = ToolReport
    context_object_name = 'report'


class ReportCreateView(CreateView):
    model = ToolReport
    form_class = ReportForm
    success_url = reverse_lazy('report_changelist')


class ReportUpdateView(UpdateView):
    model = ToolReport
    form_class = ReportForm
    success_url = reverse_lazy('report_changelist')

def load_toolbox(request):
    jobsite_id = request.GET.get('jobsite')    
    toolbox = Toolbox.objects.filter(jobsite_id=jobsite_id)
    context = {'toolbox': toolbox}
    return render(request, 'ToolOwnershipTracker/toolbox_ddl.html', context)

def load_tool(request):
    toolbox_id = request.GET.get('toolbox')    
    tool = Tool.objects.filter(toolbox_id=toolbox_id)
    context = {'tool': tool}
    return render(request, 'ToolOwnershipTracker/tool_ddl.html', context)