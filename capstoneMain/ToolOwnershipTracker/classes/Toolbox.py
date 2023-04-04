
from ToolOwnershipTracker.classes import Tool
from ToolOwnershipTracker.models import User, Toolbox, Jobsite


def ToolboxClass():
    def createToolbox(self, owner):
        if isValidJobsite(owner):
            ownerName = None
            jobsite = owner
        elif User.verifyEmailExists(owner):
            if not checkToolboxExists(self, owner):
                ownerName = owner
                jobsite = None
        else:
            raise Exception("Toolbox MUST have a Owner or a Jobsite")
            return False
        newToolbox = Toolbox(owner=ownerName, jobsite=jobsite)
        newToolbox.save()

    # tests to make sure the owner is a Jobsite
    def isValidJobsite(self, owner):
        test = list(map(str, Jobsite.objects.filter(id=owner)))
        if test.length == 0:
            return False
        return True

    # adds tool to toolbox if it does not belong somewhere
    def addTool(self, tool):
        if Tool.isUnassigned(self, tool):
            self.tools.add(tool)

    # adds removes tool from toolbox if it is in the toolbox and it is not assigned to a user
    def removeTool(self, tool):
        if self.tools.contains(tool) and not User.verifyEmailExists(self, tool.toolbox):
            self.remove.tools(tool)

    def addTool(self, tool):
        test = list(map(str, Tool.objects.filter(id=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        Tool.changeUser(tool, self.id)
        self.tools.add(tool)
        return True

    def removeTool(self, tool):
        if containsTool(self, tool):
            if tool.toolbox is None or tool.toolbox is self.id:
                self.toolbox.remove(tool)
                Tool.unassignToolbox(tool)
            else:
                raise Exception("This is assigned to a user")
                return False
        else:
            raise Exception("Tool is not in toolbox")
            return False
        return True

    def containsTool(self, tool):
        if not self.tools.contains(tool):
            return False
        return True

    # removes all tools from jobsite's toolbox
    def removeAllTools(self):
        for tools in self.toolbox.tools:
            if not removeTool(self, self.tool):
                raise Exception("Unable to remove" + tools.id)
                return False
        return True

    def checkToolboxExists(self, owner):
        if self.owner.contains(owner):
            raise Exception("That user already has a toolbox")
            return False
        return True
