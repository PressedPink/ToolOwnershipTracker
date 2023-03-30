import hashlib
import re


#import capstoneMain.ToolOwnershipTracker.models
from django.contrib.auth.models import User


class UserClass:
    def createUser(self, firstName, lastName, email, password, confirmPassword, address, phone):
        if self.checkEmail(self, email) and self.checkFirstName(self, firstName) and self.checkLastName(self, lastName) and self.checkAddress(self, address) and self.checkPhone(self, phone) and self.verifyPasswordRequirements(self, password, confirmPassword) and not self.verifyEmailExists(self,email):
            hashPass = self.hashPass(password)
            # U = basic user, S = Supervisor A = Admin
            newUser = User(firstName, lastName, email,
                       'U', hashPass, address, phone)
            newUser.save()

    def checkAddress(self, address) -> object:
        if address is None:
            raise Exception("Address may not be left blank")
            return False
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
        if self.checkFirstName(self, firstName):
            self.firstName = firstName
            self.save()

    def editLastName(self, lastName):
        if self.checkLastName(self, lastName):
            self.lastName = lastName
            self.save()

    def editAddress(self, address):
        if self.checkAddress(self, address):
            self.address = address
            self.save()

    def editEmail(self, email):
        if self.checkEmail(self, email):
            self.email = email
            self.save()

    def editPhone(self, phone):
        if self.checkPhone(self, phone):
            self.phone = phone
            self.save()

    def updatePassword(self, password):
        if self.verifyPasswordRequirements(self, password):
            self.password = self.hashPass(password)

    def verifyEmailExists(self, email):
        test = list(map(str, User.objects.filter(email=email)))
        if test.length == 0:
            return False
        return True