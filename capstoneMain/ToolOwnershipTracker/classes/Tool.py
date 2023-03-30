from capstoneMain.ToolOwnershipTracker.Users import User
from capstoneMain.ToolOwnershipTracker.classes import Jobsite, Toolbox


def Tool():
    def createTool(self):
        tool = Tool()
        tool.save()
        return True

    def deleteTool(self):
        if isUnassigned():
            self.remove(self)
            return True
        raise Exception("Unable to Remove Tool")
        return False

    def isUnassigned(self, owner, jobsite):
        if self.toolbox is None:
            return True
        return False

    def changeUser(self, owner, jobsite):
        if checkValidAssignment(self, owner, jobsite):
            self.toolbox = owner
            self.save()
            return True
        raise Exception("Unable to Change Toolbox")
        return False

    def checkValidAssignment(self, owner, jobsite):
        if (jobsite.assigned.contains(owner) and jobsite.assigned.contains(
                self.toolbox)) or jobsite.owner is owner or owner.role is 'A':
            return True
        return False

    def unassignToolbox(self):
        self.toolbox = None
        self.save()
        return True
