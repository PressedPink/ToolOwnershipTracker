from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


class UserTestForgotPassword(TestCase):

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

    def testForgotPassword(self):
        user = User.get(email="email1@gmail.com")
        oldToken = user.forgot_password_token
        resp = self.testClient.post("login/", {"Submit": "Forgot Password"}, follow=True)
        self.assertRedirects(resp, "password_reset/")
        resp = self.testClient.post("password_reset/", {"Email": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "password_reset_sent/")
        # from here, the user attempting to reset password is emailed a link they must click on
        # the user's forgot_password_token is randomly generated to a new token
        # at the link, the user must enter their email, new password, and confirm their new password
        newToken = user.forgot_password_token
        self.assertNotEqual(oldToken, newToken)
        passResetForm = "password_reset_form/" + newToken + "/"
        resp = self.testClient.post(passResetForm, {"Email": "email1@gmail.com", "Password": "newpass",
                                                    "Confirm Password": "newpass"}, follow=True)
        self.assertRedirects(resp, "password_reset_done/")
        resp = self.testClient.post("password_reset_done/", {"Submit": "Login"}, follow=True)
        self.assertRedirects(resp, "login/")
        updatedUserPassword = User.get(email="email1@gmail.com").password
        self.assertEqual(updatedUserPassword, "newpass", msg="New password did not update correctly")

