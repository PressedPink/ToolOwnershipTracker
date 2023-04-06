from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import Toolbox, Jobsite, User, Tool


class addJobsiteTests(TestCase):

    def setUp(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempAdmin = User(firstName="test", lastName="test", email="test2", password="test", address="test",
                         phone="test", role='A')
        tempAdmin.save()
        tempSupervisor = User(firstName="test", lastName="test", email="test3", password="test", address="test",
                              phone="test", role='S')
        tempSupervisor.save()

    def testPositiveWithAdmin(self):
        tempJobsite = Jobsite.createJobsite(self, "test", self.tempAdmin)
        self.assertEquals(tempJobsite.owner, self.tempAdmin)
        self.assertEquals(tempJobsite.title, "test")
        self.assertEquals(list(map(str, Jobsite.objects.filter(owner=self.tempAdmin))).toolbox > 0)

    def testPositiveWithSupervisor(self):
        tempJobsite = Jobsite.createJobsite(self, "test", self.tempSupervisor)
        self.assertEquals(tempJobsite.owner, self.tempSupervisor)
        self.assertEquals(tempJobsite.title, "test")
        self.assertEquals(list(map(str, Jobsite.objects.filter(owner=self.tempSupervisor))).toolbox > 0)

    def testNegativeWithFakeUser(self):
        self.assertRaises(Exception, Jobsite.createJobsite(self, "test", "Test"))

    def testNegativeWithFakeAdmin(self):
        self.assertRaises(Exception, Jobsite.createJobsite(self, "test", self.tempUser))


class removeJobsiteTests(TestCase):

    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempAdmin = User(firstName="test", lastName="test", email="test2", password="test", address="test",
                         phone="test",
                         role="A")
        tempAdmin.save()
        tempToolbox = Toolbox(id="1")
        tempToolbox.save()
        newTempToolbox = Toolbox(id="2")
        newTempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempAdmin, title="test", toolbox=tempToolbox)
        tempJobsite.save()
        newTempJobsite = Jobsite(id="2", owner=tempAdmin, title="test", toolbox=newTempToolbox)
        newTempJobsite.save()
        tempToolbox.jobsite = tempJobsite.id
        tempToolbox.save()
        tempTool = Tool(id="1", toolbox=newTempToolbox)
        tempTool.save()

    def testPositiveRemoval(self):
        self.assertTrue(Jobsite.removeJobsite(self.newTempJobsite))

    def testNegativeRemoval(self):
        self.assertRaises(Exception, Jobsite.removeJobsite(self.tempJobsite))


class addUserTests(TestCase):
    def setup(self):
        tempAdmin = User(firstName="test", lastName="test", email="test2", password="test", address="test",
                         phone="test",
                         role="A")
        tempAdmin.save()
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempToolbox = Toolbox(id="1")
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempAdmin, title="test", toolbox=tempToolbox)
        tempJobsite.save()

    def testPositive(self):
        self.assertIsTrue(Jobsite.addUser(self.tempJobsite, self.tempUser))
        self.assertIsTrue(self.tempJobsite.assigned.contains(self.tempUser))

    def testNegativeFakeUser(self):
        self.assertRaises(Exception, Jobsite.addUser(self.tempJobsite, "test"))

    def testNegativeUserAlreadyInJobsite(self):
        self.tempJobsite.assigned.add(self.tempUser)
        self.assertRaises(Exception, Jobsite.adddUser(self.tempJobsite, self.tempUser))


class testAssignOwner(TestCase):
    def setup(self):
        tempAdmin = User(firstName="test", lastName="test", email="test", password="test", address="test",
                         phone="test",
                         role="A")
        tempAdmin.save()
        tempToolbox = Toolbox(id="1")
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempAdmin, title="test", toolbox=tempToolbox)
        tempJobsite.save()
        tempToolbox.jobsite = tempJobsite
        tempJobsite.save()

    def testPositive(self):
        self.assertTrue(Jobsite.assignOwner(self.tempJobsite, self.tempAdmin))

    def testNegativeFakeUser(self):
        self.assertRaises(Exception, Jobsite.assignOwner(self.tempJobsite, "test"))

    def testNegativeNonAdmin(self):
        self.assertRaises(Exception, Jobsite.assignOwner(self.tempJobsite, self.tempUser))


class testChangeTitle(TestCase):
    def setup(self):
        tempAdmin = User(firstName="test", lastName="test", email="test", password="test", address="test",
                         phone="test",
                         role="A")
        tempAdmin.save()
        tempToolbox = Toolbox(id="1")
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempAdmin, title="test", toolbox=tempToolbox)
        tempJobsite.save()

    def testPositive(self):
        self.assertTrue(Jobsite.changeTitle(self.tempJobsite, "new title"))

    def testNegativeBlank(self):
        self.assertRaises(Jobsite.changeTitle(self.tempJobsite, ""))


class testRemoveUser(TestCase):
    def setup(self):
        tempUser = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        tempUser.save()
        tempAdmin = User(firstName="test", lastName="test", email="test", password="test", address="test",
                         phone="test",
                         role="A")
        tempAdmin.save()
        tempToolbox = Toolbox(id="1")
        tempToolbox.save()
        tempJobsite = Jobsite(id="1", owner=tempAdmin, title="test", toolbox=tempToolbox)
        tempJobsite.save()

    def testPositive(self):
        self.tempJobsite.assigned.add(self.tempUser)
        self.assignTrue(Jobsite.removeUser(self.tempJobsite, self.tempUser))

    def testNegativeFakeUser(self):
        self.assertRaises(Exception, Jobsite.removeUser(self.tempJobsite, "test"))

    def testNegativeNotJobsite(self):
        self.assertRaises(Exception, Jobsite.removeUser(self.tempJobsite, self.tempUser))
