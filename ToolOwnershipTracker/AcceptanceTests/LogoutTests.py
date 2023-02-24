from django.test import TestCase, Client
from ToolOwnershipTracker.base.models import user


class TestLoginSuccess(TestCase):

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

        mysupervisor = user(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phoneNumber="12621234567")
        mysupervisor.save()

        myadmin = user(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()


    def test_user_logout(self):
        user.active = True
        resp = self.testClient.post("userhome/", {"logout": True}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertFalse(user.active)

    def test_super_logout(self):
        user.active = True
        resp = self.testClient.post("superhome/", {"logout": True}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertFalse(user.active)

    def test_admin_logout(self):
        user.active = True
        resp = self.testClient.post("adminhome/", {"logout": True}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertFalse(user.active)
