from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User, Tool


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


class addToolTests(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test")
        tempJobsite.save()
        tempTool = Tool(id="1")
        tempTool.save()

    def addToolPositive(self):
        self.assertTrue(Toolbox.addTool(self.tempToolbox, self.tempTool))

    def addToolNegativeDoesNotExist(self):
        self.assertRaises(Exception, self.tempToolbox, "")

    def addToolNegativeAlreadyAssignedToJobsite(self):
        self.tempTool.toolbox = self.tempJobsite.id
        self.tempTool.save()
        self.assertRaises(Exception, Toolbox.addTool(self.tempToolbox, self.tempTool))

    def addToolNegativeAlreadyAssignedToUser(self):
        self.tempTool.toolbox = self.tempUser.email
        self.tempTool.save()
        self.assertRaises(Exception, Toolbox.addTool(self.tempToolbox, self.tempTool))
