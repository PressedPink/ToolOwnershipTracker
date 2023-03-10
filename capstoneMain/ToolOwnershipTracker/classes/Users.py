import hashlib
import re
import uuid
from re import search
from django.shortcuts import render, redirect
from django.views import View
from django.forms import models

from ToolOwnershipTracker.models import User


class UserClass():
    def createUser(self, firstName, lastName, email, password, confirmPassword, address, phone):
        checkEmail(self, email)
        checkFirstName(self, firstName)
        checkLastName(self, lastName)
        checkAddress(self, address)
        checkPhone(self, phone)
        verifyPasswordRequirements(self, password, confirmPassword)
        hashPass = hashPass(password)
        # U = basic user, S = Supervisor A = Admin
        newUser = User(firstName, lastName, email,
                       'U', hashPass, address, phone)
        newUser.save()

        def checkAddress(self, address):
            if address is None:
                raise Exception("Address may not be left blank")

        def checkFirstName(self, firstName):
            if firstName is None:
                raise Exception("First Name may not be left blank")

        def checkLastName(self, lastName):
            if lastName is None:
                raise Exception("Last Name may not be left blank")

        # Possibly device these checks into submethods todo
        def checkEmail(self, email):
            if email is None:
                raise Exception("Unique Email Required")
            test = list(map(str, User.objects.filter(email=email)))
            if test.length != 0:
                raise Exception("User already exists")
            if not '@' & '.' in email:
                raise Exception("Email is Invalid")

        def checkPhone(self, phone):
            if phone is None:
                raise Exception("Phone Number may not be left blank")
            if phone.length is 10:
                raise Exception("Please include your country code")
            if phone.length is 7:
                raise Exception("Please include your country and area codes")
            if phone.length is not 11:
                raise Exception("Please enter a valid phone number")
            tempDigit = True
            for number in phone:
                if not number.isnumeric():
                    tempDigit = False
            if tempDigit:
                raise Exception("Phone Number Invalid")

        def checkPassword(self, password):
            pw = hashPass(password)
            if self.password is not pw:
                return False
            return True

        def hashPass(self, password):
            return hashlib.md5(password)

        def verifyPasswordRequirements(self, password, confirmPassword):
            if password.length < 12:
                raise Exception("Password must be at least 12 characters")
            if not re.search('!|@|#|$|%|^|&|\\*|\\(|\\)|_|\\+|-|=', password):
                raise Exception("Password must contain a symbol")
            tempUpper = False
            tempLower = False
            tempDigit = False
            for letter in password:
                if letter.isupper():
                    tempUpper = True
                if letter.islower():
                    tempLower = True
                if letter.isdigit():
                    tempDigit = True
            if not tempUpper:
                raise Exception("Password must contain an uppercase letter")
            if not tempLower:
                raise Exception("Password must contain a lowercase letter")
            if not tempDigit:
                raise Exception("Password must contain a number")
            if firstName in password:
                raise Exception(
                    "Password may not contain any part of your name")
            if password is not confirmPassword:
                raise Exception("Passwords do not Match")

        def clearSessions(self):
            # todo clear all active sessions, set active to false
            return

        def login(self, email, password):
            if self.email.upper() is not email.upper():
                raise Exception("Email is not valid")
            if self.password is not hashlib.md5(password):
                raise Exception("Password is not correct")
            clearSessions(self)
            self.active = True

        def logout(self, request):
            # do not use
            request.clear.Sessions(self)
            self.active = False
            redirectLogin()

        def redirectProfile(self, request):
            # do not use
            return redirect('profile-page', email=request.user.email, name=request.user.firstName)

        def redirectLogin(self, resquest):
            # do not use
            return redirect('login-page')
