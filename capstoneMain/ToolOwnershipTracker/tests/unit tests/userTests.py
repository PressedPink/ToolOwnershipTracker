from ToolOwnerShipTracker.models import user
from ToolOwnerShipTracker.classes.Users import Users
from django.test import TestCase
import unittest
import django
django.setup()
from capstoneMain.ToolOwnershipTracker.models import User
import Users


class testCreateUser(TestCase):

    def setup(self):
        tempUser = User(firstName = 'test',lastName='smith',email ='test@gmail.com', role = 'U', address ='test', password = 'test',
                        phone = '11111111111', forgot_password_token = '54')                                                                                                                                                                           '5')

    def createUserFail(self):
        self.assertRaises(Exception,Users.createUser('test','test','test@gmail.com', 'test', 'test', 'test', '11111111111'))


    def createUserSuccess(self):
        self.assertTrue(Users.createUser('test','test','test2@gmail.com', 'test', 'test', 'test', '11111111111')))

class editUserInfo(TestCase):

    def setup(self):

    def changePasswordFail(self):

    def changePasswordSuccess(self):

    def changePhoneFail(self):

    def changePhoneSuccess(self):

    def changeRoleSuccess(self):

    def changeRoleFail(self):

    def changeAddressFail(self):

    def changeAddressSuccess(self):

    def changeNameFail(self):

    def changeNameSuccess(self):