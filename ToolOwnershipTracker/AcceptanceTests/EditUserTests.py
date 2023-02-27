from django.test import TestCase, Client
from ToolOwnershipTracker.base.models import User


class TestEditUserSuccess(TestCase):

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

        self.testClient.post("login/", {"email": "email1@gmail.com", "password": "userpass"}, follow=True)

    def test_edit_user_first_name(self):
        resp = self.testClient.post("/userinfo/", {"InputfirstName": "John"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.firstName, "John", "Name not changed")

    def test_edit_user_last_name(self):
        resp = self.testClient.post("/userinfo/", {"InputlastName": "Cena"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.lastName, "Cena", "Name not changed")

    def test_edit_user_email(self):
        resp = self.testClient.post("/userinfo/", {"Inputemail": "newEmail@gmail.com"}, follow=True)
        checkUser = User.objects.get(email="newEmail@gmail.com")
        self.assertEqual(checkUser.email, "newEmail@gmail.com", "Email not changed")

    def test_edit_user_password(self):
        resp = self.testClient.post("/userinfo/", {"Inputpassword": "newpass"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.password, "newpass", "Password not changed")

    def test_edit_user_address(self):
        resp = self.testClient.post("/userinfo/", {"Inputaddress": "321 N Cramer St"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.address, "321 N Cramer St", "Address not changed")

    def test_edit_user_phone(self):
        resp = self.testClient.post("/userinfo/", {"Inputphone": "14140000000"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.phoneNumber, "14140000000", "Phone not changed")

    def test_edit_user_all(self):
        resp = self.testClient.post("/userinfo/",
                                    {"InputfirstName": "John", "InputlastName": "Cena",
                                     "Inputemail": "newEmail@gmail.com",
                                     "Inputpassword": "newpass", "Inputaddress": "321 N Cramer St",
                                     "Inputphone": "14140000000"})
        checkUser = User.objects.get(email="newEmail@gmail.com")
        self.assertEqual(checkUser.firstName, "John", "Name not changed")
        self.assertEqual(checkUser.lastName, "Cena", "Name not changed")
        self.assertEqual(checkUser.email, "newEmail@gmail.com", "Email not changed")
        self.assertEqual(checkUser.password, "newpass", "Password not changed")
        self.assertEqual(checkUser.address, "321 N Cramer St", "Address not changed")
        self.assertEqual(checkUser.phoneNumber, "14140000000", "Phone not changed")


class TEstEditUserFailure(TestCase):

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

        self.testClient.post("login/", {"email": "email1@gmail.com", "password": "userpass"}, follow=True)

    def test_edit_user_missing_elements(self):
        resp = self.testClient.post("/userinfo/",
                                    {"InputfirstName": "", "InputlastName": "",
                                     "Inputemail": "",
                                     "Inputpassword": "", "Inputaddress": "",
                                     "Inputphone": ""})
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.firstName, "userfirst", "Name changed when shouldn't have")
        self.assertEqual(checkUser.lastName, "userlast", "Name changed when shouldn't have")
        self.assertEqual(checkUser.email, "email1@gmail.com", "Email changed when shouldn't have")
        self.assertEqual(checkUser.password, "userpass", "Password changed when shouldn't have")
        self.assertEqual(checkUser.address, "123 N Road St", "Address changed when shouldn't have")
        self.assertEqual(checkUser.phoneNumber, "14141234567", "Phone changed when shouldn't have")


class TestEditSuperSuccess(TestCase):

    def setup(self):
        self.testClient = Client()
        mysupervisor = User(firstName="superfirst",
                            lastName="superlast",
                            email="email2@gmail.com",
                            role="S",
                            password="superpass",
                            address="456 N Road St",
                            phoneNumber="12621234567")
        mysupervisor.save()

        self.testClient.post("login/", {"email": "email2@gmail.com", "password": "superpass"}, follow=True)

    def test_edit_super_first_name(self):
        resp = self.testClient.post("/superinfo/", {"InputfirstName": "John"}, follow=True)
        checkUser = User.objects.get(email="email1@gmail.com")
        self.assertEqual(checkUser.firstName, "John", "Name not changed")

    def test_edit_super_last_name(self):
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
        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "adminpass"}, follow=True)

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
