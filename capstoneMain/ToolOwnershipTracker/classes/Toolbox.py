from capstoneMain.ToolOwnershipTracker.Jobsite import Jobsite
from capstoneMain.ToolOwnershipTracker.classes import Tool, Users
from capstoneMain.ToolOwnershipTracker.models import User, Toolbox


def Toolbox():

    def createToolbox(self, owner):
        if isValidJobsite(owner):
            ownerName = None
            jobsite = owner
        elif User.verifyEmailExists(owner):
            ownerName = owner
            jobsite = None
        else:
            return False
        newToolbox = Toolbox(owner=ownerName, jobsite=jobsite)
        newToolbox.save()

    #tests to make sure the owner
    def isValidJobsite(self, owner):
        test = list(map(str, Jobsite.objects.filter(id=owner)))
        if test.length == 0:
            return False
        return True

    def addTool(self, tool):
        Tool.isUnassigned(self, tool)
        self.tools.add(tool)

    def removeTool(self, tool):
        Tool.isUnassigned(self, tool)
        self.remove.tools(tool)
        Tool.remove.toolbox()
