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

    #tests to make sure the owner is a Jobsite
    def isValidJobsite(self, owner):
        test = list(map(str, Jobsite.objects.filter(id=owner)))
        if test.length == 0:
            return False
        return True


    def addTool(self, tool):
        if Tool.isUnassigned(self, tool):
            self.tools.add(tool)

    def removeTool(self, tool):
        Tool.isUnassigned(self, tool)
        self.remove.tools(tool)
        Tool.remove.toolbox()

    def addTool(self, tool):
        test = list(map(str, Tool.objects.filter(id=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        self.toolbox.add(tool)
        return True

    def removeTool(self, tool):
        if containsTool(self, tool) and tool.toolbox is None or tool.toolbox is self.id:
            self.toolbox.remove(tool)
        else:
            raise Exception("This is assigned to a user")
            return False
        return True

    def containsTool(self, tool):
        test = list(map(str, Jobsite.objects.filter(tool=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        return True


    #removes all tools from jobsite's toolbox
    def removeAllTools(self):
        for tools in self.toolbox.tools:
            if not removeTool(self, self.tool):
                return False
        return True
