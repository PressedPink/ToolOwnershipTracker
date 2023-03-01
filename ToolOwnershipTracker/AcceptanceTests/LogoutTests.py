from django.test import TestCase, Client
from ToolOwnershipTracker.base.models import User


class TestLogoutSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        myuser = User(firstName="userfirst",
                      lastName="userlast",
                      email="email1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phoneNumber="14141234567")
        myuser.save()

        mysupervisor = User(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phoneNumber="12621234567")
        mysupervisor.save()

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

    def test_user_logout(self):
        resp = self.testClient.post("login/", {"Inputemail": "email1@gmail.com", "Inputpassword": "userpass"}, follow=True)
        resp = self.testClient.post("userhome/", {"Submit": "Logout"}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")

    def test_super_logout(self):
        resp = self.testClient.post("login/", {"Inputemail": "email2@gmail.com", "Inputpassword": "superpass"}, follow=True)
        resp = self.testClient.post("superhome/", {"Submit": "Logout"}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")

    def test_admin_logout(self):
        resp = self.testClient.post("login/", {"Inputemail": "email3@gmail.com", "Inputpassword": "adminpass"}, follow=True)
        resp = self.testClient.post("adminhome/", {"Submit": "Logout"}, follow=True)
        self.assertEqual("login/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")
