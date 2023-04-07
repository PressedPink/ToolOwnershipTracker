
from ToolOwnershipTracker.models import User, ToolReport


class ToolReport():

    def createToolReport(self, user, impacted, tool, time, jobsite, reportType, description):
        if User.verifyEmailExists(user):
            if checkToolorUser(tool,impacted):
                if time is None:
                    time = datetime.now()
                if checkTime(time):
                    if Jobsite.id.contains(jobsite):
                        if description is None:
                            raise Exception("Description may not be empty")
                    else:
                        raise Exception("Must have a valid Jobsite attached")
                else:
                    raise Exception("Incident occurrence must be a date")
            else:
                raise Exception("Report must have a tool or impacted user")

            newReport = ToolReport(reporter = user, created = datetime.now(), reportType=reportType, tool=tool, jobSite=jobsite, description = description)
            newReport.save()
            for users in impacted:
               if not User.verifyEmailExists(users):
                   raise Exception("Impacted Users listed contains invalid user")
               else:
                   addImpactedUser(users)

    def deleteReport(self):
        self.remove(self)

    def addImpactedUser(self, impacted):
        if not User.verifyEmailExists(impacted):
            raise Exception("User is not valid")
        else:
            self.impacted.add(impacted)
            self.save()

    def removeImpactedUser(self,user):
        self.impacted.remove(user)

    def assignTool(self, tool):
        if not Tool.id.contains(tool):
            raise Exception("Tool is not valid")
        else:
            self.tool=tool
        self.save()

    def updateDescription(self, description):
        if description is None:
            raise Exception("Description cannot be empty")
        else:
            self.description=description
        self.save()

    def changeReportType(self, reportType):
        if reportType is "R":
            self.reportType = reportType.Report
        elif reportType is "D":
            self.reportType = reportType.Damaged
        elif reportType is "I":
            self.reportType = reportType.Injury
        elif reportType is "L":
            self.reportType = reportType.Lost
        else:
            raise Exception("This is not a valid reportType")
        self.save()

    def checkTime(time):
        return isInstance(time, datetime.date)

    def checkToolorUser(tool, impacted):
        if Tool.id.contains(tool):
            return True
        if User.verifyEmailExists(impacted):
            return True
        else:
            return False
