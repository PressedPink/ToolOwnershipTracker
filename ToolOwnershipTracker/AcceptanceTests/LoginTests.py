from django.test import TestCase, Client
from base.models import user


class TestLoginSuccess(TestCase):

    def setUp(self):
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

    def test_user_login(self):
        resp = self.testClient.post("login/", {"email": "email1@gmail.com", "password": "userpass"}, follow=True)
        self.assertEqual("/userhome/", resp.request.get("PATH"))

    def test_supervisor_login(self):
        resp = self.testClient.post("login/", {"email": "email2@gmail.com", "password": "superpass"}, follow=True)
        self.assertEqual("/superhome/", resp.request.get("PATH"))

    def test_admin_login(self):
        resp = self.testClient.post("login/", {"email": "email3@gmail.com", "password": "adminpass"}, follow=True)
        self.assertEqual("/adminhome/", resp.request.get("PATH"))


class TestLoginFailure(TestCase):

    def setUp(self):
        self.testClient = Client()
        myuser = user(firstName="userfirst",
                      lastName="userlast",
                      email="email1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phoneNumber="14141234567")
        myuser.save()

    def test_invalid_username(self):
        resp = self.testClient.post("login/", {"email": "notemail@gmail.com", "password": "userpass"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.context["message"], "username or password is incorrect")

    def test_invalid_password(self):
        resp = self.testClient.post("login/", {"email": "email1@gmail.com", "password": "notpass"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.context["message"], "username or password is incorrect")
