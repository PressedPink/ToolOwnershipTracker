from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


class TestUserSignUpSuccess(TestCase):

    def setup(self):
        self.testClient = Client()

    def test_user_sign_up(self):
        resp = self.testClient.post("login/", {"submit": "Sign Up"}, follow=True)
        self.assertRedirects(resp, "usersignup/")
        resp = self.testClient.post("usersignup/", {"First Name": "John", "Last Name": "Cena",
                                                    "Email": "email1@gmail.com", "Role": "U", "Password": "userpass",
                                                    "Address": "1000 N Road St", "Phone Number": "14140000000"},
                                    follow=True)
        self.assertRedirects(resp, "login/")
        checkuser = User.get(email="email1@gmail.com")
        self.assertIsNotNone(checkuser)
        self.assertEqual("John", checkuser.firstName)
        self.assertEqual("Cena", checkuser.lastName)
        self.assertEqual("email1@gmail.com", checkuser.email)
        self.assertEqual("U", checkuser.role)
        self.assertEqual("userpass", checkuser.password)
        self.assertEqual("1000 N Road St", checkuser.address)
        self.assertEqual("14140000000", checkuser.phoneNumber)

    def test_super_sign_up(self):
        resp = self.testClient.post("login/", {"submit": "Sign Up"}, follow=True)
        self.assertRedirects(resp, "usersignup/")
        resp = self.testClient.post("usersignup/", {"First Name": "George", "Last Name": "Bush",
                                                    "Email": "email2@gmail.com", "Role": "S", "Password": "superpass",
                                                    "Address": "1000 N Road St", "Phone Number": "14140000000"},
                                    follow=True)
        self.assertRedirects(resp, "login/")
        checksuper = User.get(email="email2@gmail.com")
        self.assertIsNotNone(checksuper)
        self.assertEqual("George", checksuper.firstName)
        self.assertEqual("Bush", checksuper.lastName)
        self.assertEqual("email2@gmail.com", checksuper.email)
        self.assertEqual("S", checksuper.role)
        self.assertEqual("superpass", checksuper.password)
        self.assertEqual("1000 N Road St", checksuper.address)
        self.assertEqual("14140000000", checksuper.phoneNumber)

    def test_admin_sign_up(self):
        resp = self.testClient.post("login/", {"submit": "Sign Up"}, follow=True)
        self.assertRedirects(resp, "usersignup/")
        resp = self.testClient.post("usersignup/", {"First Name": "Bill", "Last Name": "Buckner",
                                                    "Email": "email3@gmail.com", "Role": "A", "Password": "adminpass",
                                                    "Address": "1000 N Road St", "Phone Number": "14140000000"},
                                    follow=True)
        self.assertRedirects(resp, "login/")
        checkadmin = User.get(email="email3@gmail.com")
        self.assertIsNotNone(checkadmin)
        self.assertEqual("Bill", checkadmin.firstName)
        self.assertEqual("Buckner", checkadmin.lastName)
        self.assertEqual("email3@gmail.com", checkadmin.email)
        self.assertEqual("A", checkadmin.role)
        self.assertEqual("adminpass", checkadmin.password)
        self.assertEqual("1000 N Road St", checkadmin.address)
        self.assertEqual("14140000000", checkadmin.phoneNumber)


class TestUserSignUpFailure(TestCase):

    def setup(self):
        self.testClient = Client()
        myuser = User(firstName="userfirst",
                      lastName="userlast",
                      email="user1@gmail.com",
                      role="U",
                      password="userpass",
                      address="123 N Road St",
                      phoneNumber="14141234567")
        myuser.save()

    def test_user_sign_up_empty(self):
        resp = self.testClient.post("login/", {"submit": "Sign Up"}, follow=True)
        self.assertRedirects(resp, "usersignup/")
        resp = self.testClient.post("usersignup/", {"First Name": "", "Last Name": "",
                                                    "Email": "", "Role": "", "Password": "",
                                                    "Address": "", "Phone Number": ""},
                                    follow=True)
        self.assertRedirects(resp, "usersignup/")
        self.assertEqual(1, User.objects.all.count())  # no new user was added

    def test_user_email_already_exists(self):
        resp = self.testClient.post("login/", {"submit": "Sign Up"}, follow=True)
        self.assertRedirects(resp, "usersignup/")
        resp = self.testClient.post("usersignup/", {"First Name": "Tom", "Last Name": "Sawyer",
                                                    "Email": "user1@gmail.com", "Role": "U", "Password": "userpass",
                                                    "Address": "123 N Road St", "Phone Number": "14140000000"},
                                    follow=True)
        self.assertRedirects(resp, "usersignup/")
        self.assertEqual(1, User.objects.all.count())  # no new user was added
