from django.shortcuts import render, redirect
from django.views import View
from base.models import User, UserType
from classes.profile import Profile

# For the signup.html page, which allows the user to be redirected to the signup page when successfully or unsuccesfully signing up.
class Profile(View):
    def get(self, request):
        a = request.session["email"]
        b = User.objects.get(email = a)

        return render(request, "profile.html", {"currentUser": b})

    #class EditUser(View):
    #def get(self, request):
        #m = request.session["email"]
        #return render(request, "edituser.html")
    
    #def post(self, request):
        #profile = Profile(email=request.session['email'])
        #accountType = request.POST['type']
        #password = request.POST['password']
        #email = request.POST['email']
        #phone = request.POST['phone']
        #address = request.POST['address']
        #userEdit = profile.editUser(password=str(password), accountType=str(accountType), email=str(email), phone=str(phone), address=str(address))
        #if userEdit:
            #return redirect("/edituser/")
        #else:
            #m = request.session["username"]
            #a = request.session["accountType"]
            #return render(request, "edituser.html", {"username": m, "accountType": a, "message": "invalid login"})
