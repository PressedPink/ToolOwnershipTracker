from django.test import TestCase
import capstoneMain.ToolOwnershipTracker.classes.Jobsite
import capstoneMain.ToolOwnershipTracker.models
from capstoneMain.ToolOwnershipTracker.models import User, Tool

class addReportTest(TestCase):
    def setup(self):
        admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        admin.save()
        tempTool = Tool(id="1", toolType="P")
        tempTool.save()
        tempJobsite = Jobsite(id="1", owner=admin, title="test")
        tempJobsite.save()

    def addReportPositive(self):

        def noUser():
            self.assertTrue(ToolReport.createToolReport(self, admin, None, tempTool, None, tempJobsite, R, "This is  a test"))

        def noTool():
            self.assertTrue(ToolReport.createToolReport(self, admin, admin, None, None, tempJobsite, R, "This is  a test"))

    def addReportNegative(self):

        def noUserorTool():
            self.assertRaises(Exception, ToolReport.createToolReport(self, admin, None, None, None, tempJobsite, R, "This is  a test"))

        def noDescription():
            self.assertRaises(Exception, ToolReport.createToolReport(self, admin, admin, None, None, tempJobsite, R, ""))

        def noJobsite():
            self.assertRaises(Exception, ToolReport.createToolReport(self, admin, admin, None, None, None, R, "This is a test"))

        def wrongTime():
            self.assertRaises(Exception, ToolReport.createToolReport(self, admin, admin, None, "spaghetti", tempJobsite, R, "This is a test"))

class removeReportTests(TestCase):
    admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
    admin.save()
    tempTool = Tool(id="1", toolType="P")
    tempTool.save()
    tempJobsite = Jobsite(id="1", owner=admin, title="test")
    tempJobsite.save()
    testReport = ToolReport(reporter=admin,created=datetime.now(), reportType="R", tool=None, jobSite=tempJobsite, description = "This is a test")
    testReport.save()
    assertTrue(ToolReport.deleteReport(testReport))

class editReportTest(TestCase):

    def setup(self):
        admin = User(firstName="test", lastName="test", email="test", password="test", address="test", phone="test")
        admin.save()
        tempTool = Tool(id="1", toolType="P")
        tempTool.save()
        tempJobsite = Jobsite(id="1", owner=admin, title="test")
        tempJobsite.save()
        testReport = ToolReport(reporter=admin, created=datetime.now(), reportType="R", tool=None, jobSite=tempJobsite,
                                description="This is a test")
        testReport.save()

    def addUserTest(self):
        def positiveAdd():
            assertTrue(ToolReport.addImpactedUser(testReport,admin))

        def negativeAdd():
            assertRaises(Exception, ToolReport.addImpactedUser(testReport, "test"))

    def removeUserTest(self):
        def positiveRemove():
            assertTrue(ToolReport.removeImpactedUser(testReport, admin))
            #this currently does not tell you if nothing was removed

    def UpdateTypeTest(self):
        def positiveChange():
            assertTrue(ToolReport.changeReportType(testReport, "I"))

        def negativeChange():
            assertRaises(Exception, ToolReport.changeReportType(testReport,"Spaghetti"))

