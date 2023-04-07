import unittest
from unittest import TestCase

from capstoneMain.ToolOwnershipTracker.models import Tool, User, Jobsite


class testCreateTool(TestCase):
    def testPositiveCreateTool(self):
        self.assertTrue(Tool.createTool(self))


class testRemoveTool(TestCase):
    def setup(self):
        tempTool = Tool(id="1")
        tempTool.save()
        admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        admin.save()

    def testPositiveRemoveTool(self):
        self.assertTrue(Tool.deleteTool(self.tempTool))

    def testNegativeRemoveToolAssigned(self):
        self.tempTool.toolbox = self.admin.email
        self.tempTool.save()
        self.assertRaises(Exception, self.tempTool)


class testChangeOwner(TestCase):
    def setup(self):
        admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        admin.save()
        tempTool = Tool(id="1")
        tempTool.save()
        tempJobsite = Jobsite(id="1", owner=admin, title="test")
        tempJobsite.save()

    def testPositiveUser(self):
        self.assertTrue(Tool.changeOwner(self.tempTool, self.admin))

    def testPositiveJobsite(self):
        self.assertTrue(Tool.changeOwner(self.tempTool, self.tempJobsite.id))

    def testNegativeNotaValidUser(self):
        self.assertRaises(Exception, Tool.changeOwner(self.tempTool, "@"))

    def testNegativeNotaValidJobsite(self):
        self.assertRaises(Exception, Tool.changeOwner(self.tempTool, ""))
