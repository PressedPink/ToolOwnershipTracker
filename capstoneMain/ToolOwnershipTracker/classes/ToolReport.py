


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
                    raise Exception("Incident occurance must be a date")
            else:
                raise Exception("Report must have a tool or impacted user")


    def deleteReport(self):

    def addImpactedUser(self):

    def removeImpactedUser(self):

    def assignTool(self):

    def updateDescription(self):

    def changeReportType(self):

    def checkTime(self):

        return isInstance(self, datetime.date)

    def checkToolorUser(tool, impacted):
        if Tool.id.contains(tool):
            return True
        if User.verifyEmailExists(impacted):
            return True
        else:
            return False
