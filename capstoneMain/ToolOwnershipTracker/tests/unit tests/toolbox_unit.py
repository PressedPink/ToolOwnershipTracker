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
        self.assertTrue(Toolbox.addTool(self.tempBox, self.tempTool))

    def addToolNegativeDoesNotExist(self):
        self.assertRaises(Exception, self.tempBox, "")

    def addToolNegativeAlreadyAssignedToJobsite(self):
        self.tempTool.toolbox = self.tempJobsite.id
        self.tempTool.save()
        self.assertRaises(Exception, Toolbox.addTool(self.tempBox, self.tempTool))

    def addToolNegativeAlreadyAssignedToUser(self):
        self.tempTool.toolbox = self.tempUser.email
        self.tempTool.save()
        self.assertRaises(Exception, Toolbox.addTool(self.tempBox, self.tempTool))


class removeAllTools(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test")
        tempJobsite.save()
        tempTool = Tool(id="1", owner=tempJobsite.id)
        tempTool.save()
        tempBox = Toolbox(id="1", owner=self.admin)
        tempBox.save()

    def testPositiveOneTool(self):
        self.assertTrue(Toolbox.removeAllTools(self.tempToolbox))

    def testPositiveMultipleTools(self):
        self.tempToolbox.tools.add(self.tempTool2)
        self.tempToolbox.save()
        self.assertTrue(Toolbox.removeAllTools(self.tempToolbox))

    def testNegativeToolIsAssigned(self):
        self.tempTool.toolbox = self.tempUser.email
        self.tempTool.save()
        self.tempToolbox.tools = None
        self.tempToolbox.save()
        self.tempToolbox.add(self.tempTool)
        self.tempToolbox.save()
        self.assertRaises(Exception, Toolbox.removeAllTools(self.tempToolbox))
