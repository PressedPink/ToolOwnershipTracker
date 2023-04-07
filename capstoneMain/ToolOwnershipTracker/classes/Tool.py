from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.models import Jobsite


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

    def changeUser(self, owner):
        if UserClass.checkEmail(owner):
            if UserClass.verifyEmailExists(owner):
                self.toolbox = owner
                self.save()
                return True
            else:
                raise Exception("User does not exist")
                return False
        elif checkValidAssignment(self, owner):
            self.toolbox = owner
            self.save()
        else:
            raise Exception("User does not exist")
            return False

    def checkValidAssignment(self, owner):
        if Jobsite.id.contains(owner):
            return True
        raise Exception("Invalid Jobsite")
        return False

    def unassignToolUser(self):
        self.remove.owner()
        self.save()

    def unassignToolJobsite(self):
        self.remove.jobsite()
        self.save()

    def changeLocation(self, owner, jobsite):
        unassignToolJobsite(self)
        isUnassigned(self, owner, jobsite)
        ToolboxClass.isValidJobsite()
        self.jobsite = jobsite
        self.save()
