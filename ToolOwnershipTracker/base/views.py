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
