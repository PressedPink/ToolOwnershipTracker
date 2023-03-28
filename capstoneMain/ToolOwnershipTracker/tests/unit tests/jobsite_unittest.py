from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User


class addJobsiteTests(TestCase):

    def setUp(self):
        tempUser = User(firstName = "test", lastName = "test", email = "test", password = "test", address = "test", phone = "test")
        tempUser.save()
        tempToolbox = Toolbox(id="1", owner=tempUser)
        tempToolbox.save()

    def testPositiveWithAll(self, tempUser, tempToolbox):
        tempJobsite = Jobsite(id = "1", owner = tempUser, title = "test", assigned = tempUser, toolbox = tempToolbox)
        tempJobsite.save()
        self.assertEquals(tempJobsite.id, 1)
        self.assertEquals(tempJobsite.owner, tempUser)
        self.assertEquals(tempJobsite.title, "test")
        self.assertEquals(tempJobsite.assigned, tempUser)
        self.assertEquals(tempJobsite.toolbox, tempToolbox)

    def testPositiveWithoutAssigned(self, tempUser, tempToolbox):
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test", toolbox=tempToolbox)
        tempJobsite.save()
        self.assertEquals(tempJobsite.id, 1)
        self.assertEquals(tempJobsite.owner, tempUser)
        self.assertEquals(tempJobsite.title, "test")
        self.assertIsNone (tempJobsite.assigned)
        self.assertEquals(tempJobsite.toolbox, tempToolbox)

    def testNegativeWithOwner(self, tempUser, tempToolbox):
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test", assigned = tempUser)
        tempJobsite.save()
        self.assertRaises (Exception)

    def testNegativeWithToolbox(self):
        tempJobsite = Jobsite(id="1", title="test", assigned=tempUser, toolbox=tempToolbox)
        tempJobsite.save()
        self.assertRaises (Exception)


class removeJobsiteTests(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempToolbox = Toolbox(id="1", owner=tempUser)
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test", toolbox=tempToolbox)
        tempJobsite.save()


    def testPositiveRemoval(self, tempUser, tempToolbox, tempJobsite):
        self.assertTrue(Jobsite.removeJobsite(tempJobsite))

    def testNegativeRemoval(self, tempUser, tempJobsite):
        tempJobsite.assigned.add(tempUser)
        self.assertRaises(Exception, Jobsite.removeJobsite(tempJobsite))


class addToolTests(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempToolbox = Toolbox(id="1", owner=tempUser)
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test", toolbox=tempToolbox)
        tempJobsite.save()
        tempTool = capstoneMain.Tool(id="1", toolbox=tempToolbox)

    def testPositiveAddTool(self, tempJobsite, tempTool):
        self.assertTrue(Jobsite.addTool(tempJobsite,tempTool))

    def testNegativeAddTool(self, tempTool, tempJobsite):
        tempTool.toolbox = None
        tempTool.save()
        self.assertRaises(Exception,Jobsite.addTool(tempJobsite,tempTool))


class removeToolTests(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempToolbox = Toolbox(id="1", owner=tempUser)
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempUser, title="test", toolbox=tempToolbox)
        tempJobsite.save()
        tempTool = capstoneMain.Tool(id="1", toolbox=tempToolbox)

    def testPositiveToolRemoval(self, tempTool, tempJobsite):
        self.assertTrue(Jobsite.removeTool(tempJobsite,tempTool))

    def testNegativeToolRemoval(self, tempTool, tempUser, tempJobsite):
        tempTool.user = tempUser
        tempTool.save(0)
        self.assertRaises(Exception, Jobsite.removeTool(tempJobsite,tempTool))
