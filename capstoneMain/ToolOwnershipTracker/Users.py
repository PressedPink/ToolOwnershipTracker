import hashlib
import re
import uuid
from re import search
from django.shortcuts import render, redirect
from django.views import View
from django.forms import models

import models


class User():
    def createUser(self, firstName, lastName, email, password, confirmPassword, address, phone):
        self.checkEmail(self, email)
        self.checkFirstName(self, firstName)
        self.checkLastName(self, lastName)
        self.checkAddress(self, address)
        self.checkPhone(self, phone)
        self.verifyPasswordRequirements(self, password, confirmPassword)
        hashPass = self.hashPass(password)
        # U = basic user, S = Supervisor A = Admin
        newUser = User(firstName, lastName, email,
                       'U', hashPass, address, phone)
        newUser.save()

    def checkAddress(self, address):
        if address is None:
            raise Exception("Address may not be left blank")
        return True

    def checkFirstName(self, firstName):
        if firstName is None:
            raise Exception("First Name may not be left blank")
        return True

    def checkLastName(self, lastName):
        if lastName is None:
            raise Exception("Last Name may not be left blank")
        return True

    def checkEmail(self, email):
        if email is None:
            raise Exception("Unique Email Required")
        test = list(map(str, User.objects.filter(email=email)))
        if test.length != 0:
            raise Exception("User already exists")
        if not '@' & '.' in email:
            raise Exception("Email is Invalid")
        return True

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
        return True

    def checkPassword(self, password):
        pw = self.hashPass(password)
        if self.password is not pw:
            return False
        return True

    def hashPass(self, password):
        return hashlib.md5(password)

    def verifyPasswordRequirements(self, password, confirmPassword, firstName):
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
                raise Exception("Password may not contain any part of your name")
            if password is not confirmPassword:
                raise Exception("Passwords do not Match")
        return True

    def clearSessions(self):
        # todo clear all active sessions, set active to false
        return True

    def login(self, email, password):
        if self.email.upper() is not email.upper():
            raise Exception("Email is not valid")
        if self.password is not hashlib.md5(password):
            raise Exception("Password is not correct")
        self.clearSessions(self)
        active = True
        return True

    def logout(self, request):
        request.clear.Sessions(self)
        active = False
        return True

    def editFirstName(self, firstName):
        if checkFirstName(self,firstName):
            self.firstName = firstName
            self.save()

