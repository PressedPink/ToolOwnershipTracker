from capstoneMain.ToolOwnershipTracker.Users import User
from capstoneMain.ToolOwnershipTracker.Toolbox import Toolbox
from capstoneMain.ToolOwnershipTracker.models import User, Toolbox, Jobsite, UserType


def Jobsite():
    def createJobsite(self, title, owner):
        if checkTitle(self, title) and isValid(self, owner):
            jobsite = Jobsite(owner=owner, title=title)
            tbox = Toolbox.createToolbox(jobsite=jobsite)
            jobsite.save()
            tbox.save()

    def checkTitle(self, title):
        if title is None:
            raise Exception("Name of Jobsite Cannot be left empty")
            return False
        return True

    def assignOwner(self, owner):
        if isValid(self, owner):
            self.owner = owner
            self.save()

    def addUser(self, user):
        if isValid(self, user):
            self.users.add(user)

    def changeTitle(self, title):
        if checkTitle(self, title):
            self.title = title
            self.save()

    def removeJobsite(self):
        if self.toolbox.size > 0:
            raise Exception("Cannot remove jobsite until tools are returned")
        self.remove(self)
        return True

    def removeUser(self, email):
        if self.owner == email:
            raise Exception("Cannot remove the owner")
        if isValid:
            self.assigned(email).delete()
        raise Exception("That user is not on this jobsite")

    def isValid(self, email):
        test = list(map(str, User.objects.filter(email=email)))
        userType = list(map(str, User.objects.filter(email))).role
        if test.length == 0:
            raise Exception("That user does not exist")
            return False
        if userType is not UserType.Admin or UserType.Supervisor:
            raise Exception("This user does not have the correct permissions to own a jobsite")
            return False
        return True

    def addTool(self, tool):
        if not toolbox.validTool(tool):
            raise Exception("Tool does not exist")
        self.toolbox.add(tool)
        return True

    def removeTool(self, tool):
        if containsTool(self, tool) and tool.user is None:
            self.toolbox.remove(tool)
        if tool.user is not None:
            raise Exception("This is assigned to a user")
        return True

    def containsTool(self, tool):
        test = list(map(str, Jobsite.objects.filter(tool=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        return True
