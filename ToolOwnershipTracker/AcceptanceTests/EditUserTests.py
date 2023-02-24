from django.test import TestCase, Client
from ToolOwnershipTracker.base.models import user


class TestEditUserSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        myuser = user(firstName="userfirst",
                      lastName="userlast",
                      email="email1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phoneNumber="14141234567")
        myuser.save()

    def test_edit_user_name(self):
        pass

    def test_edit_user_email(self):
        pass

    def test_edit_user_password(self):
        pass

    def test_edit_user_address(self):
        pass

    def test_edit_user_phone(self):
        pass


class TestEditSuperSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        mysupervisor = user(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phoneNumber="12621234567")
        mysupervisor.save()

    def test_edit_super_name(self):
        pass

    def test_edit_super_email(self):
        pass

    def test_edit_super_password(self):
        pass

    def test_edit_super_address(self):
        pass

    def test_edit_super_phone(self):
        pass


class TestEditAdminSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        myadmin = user(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

    def test_edit_admin_name(self):
        pass

    def test_edit_admin_email(self):
        pass

    def test_edit_admin_password(self):
        pass

    def test_edit_admin_address(self):
        pass

    def test_edit_admin_phone(self):
        pass