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
        #cannot be empty
        self.assertRaises(Exception,Users.editPhone(tempUser,''))
        #no country code
        self.assertRaises(Exception, Users.editPhone(tempUser, '4145551234'))
        #no country code or area code
        self.assertRaises(Exception, Users.editPhone(tempUser, '5551234'))
        #too many numbers
        self.assertRaises(Exception, Users.editPhone(tempUser, '141455551234'))
        #not a phone number
        self.assertRaises(Exception, Users.editPhone(tempUser, 'potato'))

    def changePhoneSuccess(self):
        self.assertTrue(Users.editPhone(tempUser, '14145551234'))

    def changeAddressFail(self):
        #cannot be left blank
        self.assertRaises(Exception,Users.editAddress(tempUser,""))

    def changeAddressSuccess(self):
        self.assertTrue(Exception,Users.editAddress(tempUser,"1234 Mitchell Ave"))


    def changeNameFail(self):

    def changeNameSuccess(self):