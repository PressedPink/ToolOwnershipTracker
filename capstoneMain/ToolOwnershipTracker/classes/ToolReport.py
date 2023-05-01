from ToolOwnershipTracker.models import User, ToolReport, Tool, Toolbox, Jobsite
from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Jobsite import JobsiteClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.classes.Tool import ToolClass
from datetime import datetime

class ToolReportClass:

    def createToolReport(self, email, toolID, toolboxID, reportType, description, jobsiteID):
        if UserClass.verifyEmailExists(self, email):
            if ToolClass.isValidTool(self, toolID):
                if ToolboxClass.checkToolboxExistsWithID(self, toolboxID):
                    time = datetime.now()
                    reporter = User.objects.get(email = email)
                    tool = Tool.objects.get(id = toolID)
                    toolbox = Toolbox.objects.get(id = toolboxID)
                    if description is not None:
                        if jobsiteID is not None:
                            if JobsiteClass.isValidJobsite(self, jobsiteID):
                                jobsite = Jobsite.objects.get(id = jobsiteID)
                            else:
                                raise Exception("Jobsite does not exist!")
                        else:
                            jobsite = None
                        newReport = ToolReport(reporter = reporter, created = time, reportType = reportType, tool = tool, toolbox = toolbox, jobsite = jobsite, description = description)
                        newReport.save()
                        return True
                    else:
                        raise Exception("Description must not be empty!")
                else:
                    raise Exception("Toolbox does not exist!")
            else:
                raise Exception("Tool does not exist!")
        else:
            raise Exception("User does not exist!")

    def deleteReport(self, reportID):
        if ToolReportClass.isValidReport(self, reportID):
            report = ToolReport.objects.get(id=reportID)
            report.delete()
            return True
        else:
            raise Exception("Tool report does not exist!")

    def isValidReport(self, reportID):
        test = list(map(str, ToolReport.objects.filter(id = reportID)))
        if len(test) == 0:
            return False
        else:
            return True