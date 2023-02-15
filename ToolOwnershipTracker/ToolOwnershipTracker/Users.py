import hashlib
import re
import uuid
from re import search

from django.forms import models

from ToolOwnershipTracker.base.models import user


class User():
    def createUser(self, firstName, lastName, email, role, password, confirmPassword, address, phone):
        if email is None:
            raise Exception("Unique Email Required")
        test = list(map(str, user.objects.filter(email=email)))
        if test.length != 0:
            raise Exception("User already exists")
        if firstName is None:
            raise Exception("First Name may not be left blank")
        if lastName is None:
            raise Exception("Last Name may not be left blank")
        if role is None:
            raise Exception("Must select a user type")
        if address is None:
            raise Exception("Address may not be left blank")
        if phone is None:
            raise Exception("Phone Number may not be left blank")
        #phone length
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
        if not '@' & '.' in email:
            raise Exception("Email is Invalid")
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
        hashPass = hashlib.md5(password)
        newUser = user(firstName, lastName,email, role, hashPass, address, phone)
        newUser.save()

        def checkPassword(self, password):
            pw = hashlib.md5(password)
            if this.password is not pw:
                return False
            return True

