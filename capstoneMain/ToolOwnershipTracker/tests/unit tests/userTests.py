from . import models
from .models import User
from capstoneMain.ToolOwnerShipTracker.classes.Users import UsersClass
from django.test import TestCase
import unittest
import django
django.setup()


class TestLogin(unittest.TestCase):
    def populate_db(self):
        user = User(username='testUser', email='test@example.com')
        user.set_password('testPassword')
        db.session.add(user)
        db.session.commit()

    def login(self):
        self.client.post('/auth/login', data={
            'username': 'testUser',
            'password': 'testPassword',
        })

    def testLoginSuccess(self):
        self.login()
        assert response.status_code == 200
        
class TestEditUser(unittest.TestCase):     
     def populate_db(self):
        user = User(username='testUser', email='test@example.com')
        user.set_password('testPassword')
        db.session.add(user)
        db.session.commit()
       
