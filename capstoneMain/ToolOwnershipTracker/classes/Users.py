import uuid
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import re
import uuid

# import capstoneMain.ToolOwnershipTracker.models
from ToolOwnershipTracker.models import User
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass



class UserClass:
    # if role does not work, change 'U' to UserType.User
    def createUser(self, firstName, lastName, email, password, confirmPassword, address, phone, role):
        if UserClass.checkEmail(self, email):
            if UserClass.checkFirstName(self, firstName):
                if UserClass.checkLastName(self, lastName):
                    if UserClass.checkAddress(self, address):
                        if UserClass.checkPhone(self, phone):
                            if UserClass.verifyPasswordRequirements(self, password,confirmPassword):
                                if not UserClass.verifyEmailExists(self, email):
                                    hashPass = UserClass.hashPass(password)
                                    # U = basic user, S = Supervisor A = Admin
                                    newUser = User(firstName=firstName, lastName=lastName, email=email, role=role, password=hashPass, address=address, phone=phone, forget_password_token = hashPass)
                                    newUser.save()
                                    if(role != "A"):
                                        ToolboxClass.createUserToolbox(self, email)
            
    def checkAddress(self, address):
        if address is None:
            raise Exception("Address may not be left blank!")
            return False
        return True

    def checkFirstName(self, firstName):
        if firstName is None:
            raise Exception("First name may not be left blank!")
        return True

    def checkLastName(self, lastName):
        if lastName is None:
            raise Exception("Last name may not be left blank!")
        return True


        # Possibly device these checks into submethods todo

    def checkEmail(self, email):
        if email is None:
            raise Exception("Email may not be left blank!")
        test = list(map(str, User.objects.filter(email=email)))
        if len(test) != 0:
            raise Exception("User already exists!")
        else:
            return True
        # removed as regex is handled in input fields
        # if not '@' & '.' in email:
            # raise Exception("Email is Invalid")

    def checkPhone(self, phone):
        num = len(phone)
        if phone is None:
            raise Exception("Phone number may not be left blank!")
        if len(phone) == 7:
            raise Exception("Please include your area code!")
        if len(phone) > 12:
            raise Exception("Please enter a valid phone number!")
        tempDigit = True
        for number in phone:
            if not number.isnumeric() or not "-":
                tempDigit = False
            if not tempDigit:
                raise Exception("Phone number invalid!")

        return True

    def checkPassword(self, password):
        pw = self.hashPass(password)
        if self.password is not pw:
            return False
        return True

    def hashPass(password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def verifyPasswordRequirements(self, password, confirmPassword):
        # firstName = self.firstName

        if len(password) < 12:
            raise Exception("Password must be at least 12 characters!")
        if not re.search('!|@|#|$|%|^|&|\\*|\\(|\\)|_|\\+|-|=', password):
            raise Exception("Password must contain a symbol!")
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
            raise Exception("Password must contain an uppercase letter!")
        if not tempLower:
            raise Exception("Password must contain a lowercase letter!")
        if not tempDigit:
            raise Exception("Password must contain a number!")

        # if firstName in password:
            # raise Exception(
            # "Password may not contain any part of your name")
        if password != confirmPassword:
            raise Exception("Passwords do not match!")
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
        if UserClass.checkAddress(self, address):
            self.address = address
            self.save()

    def editEmail(self, email):
        if UserClass.checkEmail(self, email):
            self.email = email
            self.save()

    def editPhone(self, phone):
        if UserClass.checkPhone(self, phone):
            self.phone = phone
            self.save()

    def updatePassword(self, password):

        self.password = UserClass.hashPass(password)
        return True

    def check_reset_password_token(email, token):
        try:
            user = User.objects.get(email=email)
            return user.forget_password_token == token
        except User.DoesNotExist:
            return False

    def send_forget_password_mail(email, token):
        subject = 'Your password reset link'
        message = f'Hello, click the following link to be redirected to form to reset your password: http://127.0.0.1:8000/password_reset_form/{token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        return True


    def forget_password(email):

        try:
            test = list(map(str, User.objects.filter(email=email)))
        except Exception as e:
            print(e)
            raise Exception("Email is not valid!")

        token = str(uuid.uuid4())
        tempUser = User.objects.get(email=email)
        tempUser.forget_password_token = token
        tempUser.save()

        UserClass.send_forget_password_mail(email, token)
        return True


    def change_password(email, password, confirmPassword):
        try:

            test = list(map(str, User.objects.filter(email=email)))
        except:
            raise Exception("Email is not valid!")


        tempUser = User.objects.get(email=email)
        if (UserClass.verifyPasswordRequirements(tempUser, password, confirmPassword)):
            UserClass.updatePassword(tempUser, password)
            tempUser.forget_password_token = ""
            tempUser.save()
            return True

    def verifyEmailExists(self, email):
        test = list(map(str, User.objects.filter(email=email)))
        if len(test) == 0:
            return False
        return True

