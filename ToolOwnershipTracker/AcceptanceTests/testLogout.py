from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


class TestLogoutSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        myuser = User(firstName="userfirst",
                      lastName="userlast",
                      email="email1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phone="14141234567",
                      active=False)
        myuser.save()

        mysupervisor = User(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phone="12621234567",
                            active=False)
        mysupervisor.save()

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phone="14147654321",
                       active=False)
        myadmin.save()

    def test_user_logout(self):
        self.testClient.post("login/", {"Inputemail": "email1@gmail.com", "Inputpassword": "userpass"}, follow=True)
        self.assertTrue(User.objects.get(email="email1@gmail.com").active, True)
        resp = self.testClient.post("userhome/", {"Submit": "Logout"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")
        self.assertFalse(User.objects.get(email="email1@gmail.com").active)

    def test_super_logout(self):
        self.testClient.post("login/", {"Inputemail": "email2@gmail.com", "Inputpassword": "superpass"}, follow=True)
        self.assertTrue(User.objects.get(email="email2@gmail.com").active)
        resp = self.testClient.post("superhome/", {"Submit": "Logout"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")
        self.assertFalse(User.objects.get(email="email2@gmail.com").active)

    def test_admin_logout(self):
        self.testClient.post("login/", {"Inputemail": "email3@gmail.com", "Inputpassword": "adminpass"}, follow=True)
        self.assertTrue(User.objects.get(email="email3@gmail.com").active)
        resp = self.testClient.post("adminhome/", {"Submit": "Logout"}, follow=True)
        self.assertRedirects(resp, "login/")
        self.assertEqual(resp.session["email"], None, msg="Session key not equal to User's email")
        self.assertFalse(User.objects.get(email="email3@gmail.com").active)
