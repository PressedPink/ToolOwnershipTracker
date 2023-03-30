from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User


class addToolboxTests(TestCase):
    def setup(self):
        self.admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        self.tempToolbox = Toolbox(id="1", tools=None, owner=admin)
        self.tempTool = capstoneMain.Tool(id="1")
        self.admin.save()
        self.tempToolbox.save()
        self.tempTool.save()

    def addToolboxPositive(self):
        self.assertTrue(Toolbox.createToolbox(self.tempToolbox, 1, self.admin))

    def addToolboxNegative(self):
        self.assertRaises(Exception,)
