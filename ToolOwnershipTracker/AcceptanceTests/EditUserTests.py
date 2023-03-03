from django.test import TestCase, Client
from capstoneMain.ToolOwnershipTracker.models import User


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

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

        # admin logs in to edit user info and supervisor info
        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "adminpass"}, follow=True)

    def test_edit_user_first_name(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"InputfirstName": "John"}, follow=True)
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.firstName, "John", msg="Name not changed")

    def test_edit_user_last_name(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"InputlastName": "Cena"}, follow=True)
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.lastName, "Cena", msg="Name not changed")

    def test_edit_user_email(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"Inputemail": "newemail@gmail.com"}, follow=True)
        checkuser = User.get(email="newemail@gmail.com")
        self.assertEqual(checkuser.email, "newemail@gmail.com")

    def test_edit_user_role(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"Inputrole": "S"}, follow=True)
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.role, "S", msg="Role not changed")

    def test_edit_user_password(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"Inputpassword": "newpassword"}, follow=True)
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.password, "newpassword", msg="Password not changed")

    def test_edit_user_address(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"Inputaddress": "321 N Cramer St"}, follow=True)
        checkUser = User.get(email="email1@gmail.com")
        self.assertEqual(checkUser.address, "321 N Cramer St", msg="Address not changed")

    def test_edit_user_phone(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit", {"Inputphone": "14140000000"}, follow=True)
        checkUser = User.get(email="email1@gmail.com")
        self.assertEqual(checkUser.phoneNumber, "14140000000", msg="Phone not changed")

    def test_edit_user_all(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        resp = self.testClient.post("/email1@gmail.comInfo/edit/",
                                    {"InputfirstName": "John", "InputlastName": "Cena",
                                     "Inputemail": "newEmail@gmail.com", "Inputrole": "S",
                                     "Inputpassword": "newpass", "Inputaddress": "321 N Cramer St",
                                     "Inputphone": "14140000000"})
        checkuser = User.get(email="newEmail@gmail.com")
        self.assertEqual(checkuser.firstName, "John", msg="Name not changed")
        self.assertEqual(checkuser.lastName, "Cena", msg="Name not changed")
        self.assertEqual(checkuser.email, "newEmail@gmail.com", msg="Email not changed")
        self.assertEqual(checkuser.role, "S", msg="Role not changed")
        self.assertEqual(checkuser.password, "newpass", msg="Password not changed")
        self.assertEqual(checkuser.address, "321 N Cramer St", msg="Address not changed")
        self.assertEqual(checkuser.phoneNumber, "14140000000", msg="Phone not changed")


class TestEditUserFailure(TestCase):

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
                                     "Inputemail": "", "Inputrole": "",
                                     "Inputpassword": "", "Inputaddress": "",
                                     "Inputphone": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.firstName, "userfirst", msg="Name changed when shouldn't have")
        self.assertEqual(checkuser.lastName, "userlast", msg="Name changed when shouldn't have")
        self.assertEqual(checkuser.email, "email1@gmail.com", msg="Email changed when shouldn't have")
        self.assertEqual(checkuser.role, "U", msg="Role changed when shouldn't have")
        self.assertEqual(checkuser.password, "userpass", msg="Password changed when shouldn't have")
        self.assertEqual(checkuser.address, "123 N Road St", msg="Address changed when shouldn't have")
        self.assertEqual(checkuser.phoneNumber, "14141234567", msg="Phone changed when shouldn't have")


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
        checkUser = User.get(email="email1@gmail.com")
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
