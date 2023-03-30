from capstoneMain.ToolOwnershipTracker.Users import User
from capstoneMain.ToolOwnershipTracker.classes import Toolbox
from capstoneMain.ToolOwnershipTracker.models import User, Toolbox, Jobsite, UserType, Tool


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
        if User.verifyEmailExists(self, user):
            self.users.add(user)

    def changeTitle(self, title):
        if checkTitle(self, title):
            self.title = title
            self.save()

    def removeJobsite(self):
        if self.toolbox.tools is not None:
            raise Exception("Cannot remove jobsite until tools are returned")
            return False
        self.remove(self)
        return True

    #removes all tools from jobsite's toolbox
    def removeAllTools(self):
        for tools in self.toolbox.tools:
            if not removeTool(self, self.tool):
                return False
        return True


    def isInJobsite(self, email):
        if not self.assigned.contains(email):
            raise Exception("This user is not assigned to this jobsite")
            return False
        return True

    def removeUser(self, email):
        if isInJobsite(self,email):
            self.assigned.remove(email)
            return True
        return False

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
