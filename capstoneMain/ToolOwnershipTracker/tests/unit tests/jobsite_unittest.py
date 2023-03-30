from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User


class addJobsiteTests(TestCase):

    def setUp(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempAdmin = User(firstName="test", lastName="test", email="test2", password="test", address="test",
                         phone="test", role='A')
        tempAdmin.save()
        tempSupervisor = User(firstName="test", lastName="test", email="test2", password="test", address="test",
                              phone="test", role='S')
        tempSupervisor.save()

    def testPositiveWithAdmin(self, tempAdmin):
        tempJobsite = Jobsite.createJobsite(self, "test", tempAdmin)
        self.assertEquals(tempJobsite.owner, tempAdmin)
        self.assertEquals(tempJobsite.title, "test")
        self.assertEquals(list(map(str, Jobsite.objects.filter(owner=tempAdmin))).toolbox > 0)

    def testPositiveWithSupervisor(self, tempSupervisor):
        tempJobsite = Jobsite.createJobsite(self, "test", tempSupervisor)
        self.assertEquals(tempJobsite.owner, tempSupervisor)
        self.assertEquals(tempJobsite.title, "test")
        self.assertEquals(list(map(str, Jobsite.objects.filter(owner=tempSupervisor))).toolbox > 0)

    def testNegativeWithFakeUser(self):
        self.assertRaises(Exception, Jobsite.createJobsite(self, "test", "Test"))

    def testNegativeWithFakeAdmin(self, tempUser):
        self.assertRaises(Exception, Jobsite.createJobsite(self, "test", tempUser))


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
        self.assertTrue(Jobsite.addTool(tempJobsite, tempTool))

    def testNegativeAddTool(self, tempTool, tempJobsite):
        tempTool.toolbox = None
        tempTool.save()
        self.assertRaises(Exception, Jobsite.addTool(tempJobsite, tempTool))


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
        self.assertTrue(Jobsite.removeTool(tempJobsite, tempTool))

    def testNegativeToolRemoval(self, tempTool, tempUser, tempJobsite):
        tempTool.user = tempUser
        tempTool.save(0)
        self.assertRaises(Exception, Jobsite.removeTool(tempJobsite, tempTool))
