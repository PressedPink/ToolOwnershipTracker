from capstoneMain.ToolOwnershipTracker.Users import User
from capstoneMain.ToolOwnershipTracker.classes import Jobsite


def Tool():
    def createTool(self):
        tool = Tool(self)
        tool.save()

    def deleteTool(self):
        isUnassigned()
        self.remove(self)

    def isUnassigned(self, owner, jobsite):
        if owner is not None:
            raise Exception("This tool is already assigned to a User")
        if jobsite is not None:
            raise Exception("This tool is already in another jobsite's toolbox")
        return True

    def changeUser(self, owner):
        unassignToolUser(self)
        checkValidAssignment(self,owner)
        self.owner = owner
        self.save()

    def checkValidAssignment(self,owner):
        test = list(map(str, Jobsite.objects.filter(assigned=owner)))
        if not test.contains(owner):
            raise Exception("This user does not have access to this Jobsite and Tools")

    def unassignToolUser(self):
        self.remove.owner()
        self.save()

    def unassignToolJobsite(self):
        self.remove.jobsite()
        self.save()

    def changeLocation(self, owner, jobsite):
        unassignToolJobsite(self)
        isUnassigned(self, owner, jobsite)
        self.jobsite = jobsite
        self.save()
