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
        self.testClient.post("/email1@gmail.comInfo/edit/",
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

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "userpass"}, follow=True)

    def test_edit_user_missing_first(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"InputfirstName": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.firstName, "userfirst", "Name changed when shouldn't have")

    def test_edit_user_missing_last(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"InputlastName": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.lastName, "userlast", "Name changed when shouldn't have")

    def test_edit_user_missing_email(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"Inputemail": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.email, "email1@gmail.com", "Email changed when shouldn't have")

    def test_edit_user_missing_role(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"Inputrole": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.role, "U", "Role changed when shouldn't have")

    def test_edit_user_missing_password(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"Inputpassword": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.password, "userpass", "Password changed when shouldn't have")

    def test_edit_user_missing_address(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"Inputaddress": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.address, "123 N Road St", "Address changed when shouldn't have")

    def test_edit_user_missing_phone(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/", {"Inputphone": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.phoneNumber, "14141234567", "Phone changed when shouldn't have")

    def test_edit_user_missing_all(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email1@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/")
        resp = self.testClient.post("/email1@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email1@gmail.comInfo/edit/")
        self.testClient.post("/email1@gmail.comInfo/edit/",
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

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "userpass"}, follow=True)

    def test_edit_super_first_name(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"InputfirstName": "John"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.firstName, "John", msg="Name not changed")

    def test_edit_super_last_name(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"InputlastName": "Cena"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.lastName, "Cena", msg="Name not changed")

    def test_edit_super_email(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"Inputemail": "newemail@gmail.com"}, follow=True)
        checkuser = User.get(email="newemail@gmail.com")
        self.assertEqual(checkuser.email, "newemail@gmail.com")

    def test_edit_super_role(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"Inputrole": "U"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.role, "U", msg="Role not changed")

    def test_edit_super_password(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"Inputpassword": "newpass"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.password, "newpass", msg="Password not changed")

    def test_edit_super_address(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"Inputaddress": "123 S Road St"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.address, "123 S Road St", msg="Address not changed")

    def test_edit_super_phone(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit", {"Inputphone": "14140000000"}, follow=True)
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.phoneNumber, "14140000000", msg="Phone not changed")

    def test_edit_super_all(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/",
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


class TestEditSuperFailure(TestCase):

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

        myadmin = User(firstName="adminfirst",
                       lastName="adminlast",
                       email="email3@gmail.com",
                       role="A",
                       password="adminpass",
                       address="789 N Road St",
                       phoneNumber="14147654321")
        myadmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "userpass"}, follow=True)

    def test_edit_super_missing_first(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"InputfirstName": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.firstName, "superfirst", "Name changed when shouldn't have")

    def test_edit_super_missing_last(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"InputlastName": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.lastName, "superlast", "Name changed when shouldn't have")

    def test_edit_super_missing_email(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"Inputemail": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.email, "email2@gmail.com", "Email changed when shouldn't have")

    def test_edit_super_missing_role(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"Inputrole": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.role, "S", "Role changed when shouldn't have")

    def test_edit_super_missing_password(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"Inputpassword": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.password, "superpass", "Password changed when shouldn't have")

    def test_edit_super_missing_address(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"Inputaddress": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.address, "456 N Road St", "Address changed when shouldn't have")

    def test_edit_super_missing_phone(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/", {"Inputphone": ""})
        checkuser = User.get(email="email2@gmail.com")
        self.assertEqual(checkuser.phoneNumber, "12621234567", "Phone changed when shouldn't have")

    def test_edit_super_missing_all(self):
        resp = self.testClient.post("/adminhome/", {"Submit": "/listofusers/"}, follow=True)
        self.assertRedirects(resp, "/listofusers/")
        resp = self.testClient.post("/listofusers/", {"Submit": "email2@gmail.com"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/")
        resp = self.testClient.post("/email2@gmail.comInfo/", {"Submit": "edit"}, follow=True)
        self.assertRedirects(resp, "/email2@gmail.comInfo/edit/")
        self.testClient.post("/email2@gmail.comInfo/edit/",
                             {"InputfirstName": "", "InputlastName": "",
                              "Inputemail": "", "Inputrole": "",
                              "Inputpassword": "", "Inputaddress": "",
                              "Inputphone": ""})
        checkuser = User.get(email="email1@gmail.com")
        self.assertEqual(checkuser.firstName, "superfirst", msg="Name changed when shouldn't have")
        self.assertEqual(checkuser.lastName, "superlast", msg="Name changed when shouldn't have")
        self.assertEqual(checkuser.email, "email2@gmail.com", msg="Email changed when shouldn't have")
        self.assertEqual(checkuser.role, "S", msg="Role changed when shouldn't have")
        self.assertEqual(checkuser.password, "superpass", msg="Password changed when shouldn't have")
        self.assertEqual(checkuser.address, "456 N Road St", msg="Address changed when shouldn't have")
        self.assertEqual(checkuser.phoneNumber, "12621234567", msg="Phone changed when shouldn't have")


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

        otheradmin = User(firstName="otherfirst",
                          lastName="otherlast",
                          email="otheradmin@gmail.com",
                          role="A",
                          password="otherpass",
                          address="123 Main St",
                          phoneNumber="14140000000")
        otheradmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "adminpass"}, follow=True)

    def test_edit_admin_first(self):
        pass

    def test_edit_admin_last(self):
        pass

    def test_edit_admin_email(self):
        pass

    def test_edit_admin_role(self):
        pass

    def test_edit_admin_password(self):
        pass

    def test_edit_admin_address(self):
        pass

    def test_edit_admin_phone(self):
        pass

    def test_edit_admin_all(self):
        pass


class TestEditAdminFailure(TestCase):

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

        otheradmin = User(firstName="otherfirst",
                          lastName="otherlast",
                          email="otheradmin@gmail.com",
                          role="A",
                          password="otherpass",
                          address="123 Main St",
                          phoneNumber="14140000000")
        otheradmin.save()

        self.testClient.post("login/", {"email": "email3@gmail.com", "password": "adminpass"}, follow=True)

    def test_edit_admin_missing_first(self):
        pass

    def test_edit_admin_missing_last(self):
        pass

    def test_edit_admin_missing_email(self):
        pass

    def test_edit_admin_missing_role(self):
        pass

    def test_edit_admin_missing_password(self):
        pass

    def test_edit_admin_missing_address(self):
        pass

    def test_edit_admin_missing_phone(self):
        pass

    def test_edit_admin_missing_all(self):
        pass
