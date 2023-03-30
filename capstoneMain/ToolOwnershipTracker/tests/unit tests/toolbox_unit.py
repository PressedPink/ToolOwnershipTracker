from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User


class addToolboxTests(TestCase):
    def setup(self):
        admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        admin.save()
        tempJobsite = Jobsite(id="1", owner=admin, title="test")
        tempJobsite.save()

    def addToolboxPositiveWithUser(self):
        self.assertTrue(Toolbox.createToolbox(self, self.admin.email))

    def addToolboxPositiveWithJobsite(self):
        self.assertTrue(Toolbox.createToolbox(self, self.tempJobsite.id))

    def addToolboxNegativeNoOwnerOrJobsite(self):
        self.assertRaises(Exception, Toolbox.createToolbox(self, ""))

    def addToolboxNegativeAlreadyExists(self):
        tempBox = Toolbox(id="1", owner=self.admin)
        tempBox.save()
        self.assertRaises(Exception, Toolbox.createToolbox(self, self.admin.email))
