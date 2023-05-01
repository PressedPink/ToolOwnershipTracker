from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


class TestUserForgotPassword(TestCase):

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

    def test_ForgotPassword(self):
        oldToken = User.get(email="email1@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")
        # from here, the user attempting to reset password is emailed a link they must click on
        # the user's forgot_password_token is randomly generated to a new token
        # at the link, the user must enter their email, new password, and confirm their new password
        newToken = User.get(email="email1@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email1@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "newpass"}, follow=True)
        self.assertRedirects(resp, "password_reset_done/")
        resp = self.testClient.post("password_reset_done/", {"Submit": "Login"}, follow=True)
        self.assertRedirects(resp, "login/")

        updatedUserPassword = User.get(email="email1@gmail.com").password
        self.assertEqual(updatedUserPassword, "newpass", msg="New password did not update correctly")


class TestSuperForgotPassword(TestCase):

    def setup(self):
        self.testClient = Client()
        mysupervisor = User(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phone="12621234567",
                            active=False)
        mysupervisor.save()

    def test_ForgotPassword(self):
        oldToken = User.get(email="email2@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")
        # from here, the user attempting to reset password is emailed a link they must click on
        # the user's forgot_password_token is randomly generated to a new token
        # at the link, the user must enter their email, new password, and confirm their new password
        newToken = User.get(email="email2@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email2@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "newpass"}, follow=True)
        self.assertRedirects(resp, "password_reset_done/")
        resp = self.testClient.post("password_reset_done/", {"Submit": "Login"}, follow=True)
        self.assertRedirects(resp, "login/")

        updatedSuperPassword = User.get(email="email2@gmail.com").password
        self.assertEqual(updatedSuperPassword, "newpass", msg="New password did not update correctly")


class TestAdminForgotPassword(TestCase):

    def setup(self):
        self.testClient = Client()
        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phone="14147654321",
                       active=False)
        myadmin.save()

    def test_ForgotPassword(self):
        oldToken = User.get(email="email3@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email3@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")
        # from here, the user attempting to reset password is emailed a link they must click on
        # the user's forgot_password_token is randomly generated to a new token
        # at the link, the user must enter their email, new password, and confirm their new password
        newToken = User.get(email="email3@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email3@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "newpass"}, follow=True)
        self.assertRedirects(resp, "password_reset_done/")
        resp = self.testClient.post("password_reset_done/", {"Submit": "Login"}, follow=True)
        self.assertRedirects(resp, "login/")

        updatedUserPassword = User.get(email="email3@gmail.com").password
        self.assertEqual(updatedUserPassword, "newpass", msg="New password did not update correctly")


class TestForgotPasswordFailure(TestCase):

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

    def test_forgot_password_empty(self):
        oldToken = User.get(email="email1@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")

        newToken = User.get(email="email1@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email1@gmail.com", "Password": "",
                                                    "Confirm Password": ""}, follow=True)
        self.assertRedirects(resp, passResetForm)
        # Make sure password did not change
        self.assertEqual("userpass", User.get(email="email1@gmail.com").password,
                         msg="Password changed when it shouldn't have")

    def test_password_not_matching(self):
        oldToken = User.get(email="email1@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")

        newToken = User.get(email="email1@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email1@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "passnew"}, follow=True)
        self.assertRedirects(resp, passResetForm)
        # Make sure password did not change
        self.assertEqual("userpass", User.get(email="email1@gmail.com").password,
                         msg="Password changed when it shouldn't have")

    def test_email_not_matching(self):
        oldToken = User.get(email="email1@gmail.com").forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")

        newToken = User.get(email="email1@gmail.com").forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "otheremail@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "newpass"}, follow=True)
        self.assertRedirects(resp, passResetForm)
        # Make sure password did not change
        self.assertEqual("userpass", User.get(email="email1@gmail.com").password,
                         msg="Password changed when it shouldn't have")
