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
        tempUser = User(firstName='test', lastName='smith', email='test@gmail.com', role='U', address='test',
                        password='test',
                        phone='11111111111', forgot_password_token='54')

    def changePasswordFail(self):
        #is not 12 characters
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'Potato1000!', 'Potato1000!'))
        #missing special character
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'Potato100000', 'Potato100000'))
        #missing uppercase character
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'potato!10000', 'potato!10000'))
        #missing lowercase character
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'POTATO!10000', 'POTATO!10000'))
        #missing number
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'POTATo!!!!!!', 'POTATo!!!!!!'))
        #passwords do not match
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'potatO10000!', 'Tomato10000!'))
        #contains users name
        self.assertRaises(Exception, Users.changePassword(tempUser.email, 'test10000000', 'test10000000'))
        #email is invalid
        self.assertRaises(Exception, Users.changePassword('fake@gmail.com', 'Potato1000!!', 'Potato1000!!'))

    def changePasswordSuccess(self):
        self.assertTrue(Users.changePassword(tempUser.email, 'Potato1000!!', 'Potato1000!!')


    def changePhoneFail(self):

    def changePhoneSuccess(self):

    def changeRoleSuccess(self):

    def changeRoleFail(self):

    def changeAddressFail(self):

    def changeAddressSuccess(self):

    def changeNameFail(self):

    def changeNameSuccess(self):