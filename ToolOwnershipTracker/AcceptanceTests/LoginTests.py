from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


class TestLoginSuccess(TestCase):

    def setUp(self):
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

    def test_user_login(self):
        resp = self.testClient.post("login/", {"Inputemail": "email1@gmail.com", "Inputpassword": "userpass"}, follow=True)
        self.assertEqual("/userhome/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], "email1@gmail.com", msg="Session key not equal to User's email")

    def test_supervisor_login(self):
        resp = self.testClient.post("login/", {"Inputemail": "email2@gmail.com", "Inputpassword": "superpass"}, follow=True)
        self.assertEqual("/superhome/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], "email2@gmail.com", msg="Session key not equal to User's email")

    def test_admin_login(self):
        resp = self.testClient.post("login/", {"Inputemail": "email3@gmail.com", "Inputpassword": "adminpass"}, follow=True)
        self.assertEqual("/adminhome/", resp.request.get("PATH"))
        self.assertEqual(resp.session["email"], "email3@gmail.com", msg="Session key not equal to User's email")


class TestLoginFailure(TestCase):

    def setUp(self):
        self.testClient = Client()
        myuser = User(firstName="userfirst",
                      lastName="userlast",
                      email="email1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phoneNumber="14141234567")
        myuser.save()

    def test_invalid_username(self):
        resp = self.testClient.post("login/", {"Inputemail": "notemail@gmail.com", "Inputpassword": "userpass"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.context["message"], "username or password is incorrect")

    def test_invalid_password(self):
        resp = self.testClient.post("login/", {"Inputemail": "email1@gmail.com", "Inputpassword": "notpass"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.context["message"], "username or password is incorrect")
