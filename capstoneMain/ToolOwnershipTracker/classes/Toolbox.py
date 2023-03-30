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

    #adds tool to toolbox if it does not belong somewhere
    def addTool(self, tool):
        if Tool.isUnassigned(self, tool):
            self.tools.add(tool)

    #adds removes tool from toolbox if it is in the toolbox and it is not assigned to a user
    def removeTool(self, tool):
        if self.tools.contains(tool) and not User.verifyEmailExists(self, tool.toolbox):
            self.remove.tools(tool)

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
            tool.toolbox = None
        else:
            raise Exception("This is assigned to a user")
            return False
        return True

    def containsTool(self, tool):
      if not self.tools.contains(tool):
            raise Exception("Tool does not exist")
            return False
        return True

    #removes all tools from jobsite's toolbox
    def removeAllTools(self):
        for tools in self.toolbox.tools:
            if not removeTool(self, self.tool):
                return False
        return True
