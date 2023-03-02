from capstoneMain.ToolOwnershipTracker.Users import User


def Jobsite():
    def createJobsite(self, title, owner):
        checkTitle(self, title)
        isValid(self, owner)
        jobsite = Jobsite(title, owner)
        jobsite.save()

    def checkTitle(self, title):
        if title is None:
            raise Exception("Name of Jobsite Cannot be left empty")
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

    def removeUser(self, email):
        if self.owner == email:
            raise Exception("Cannot remove the owner")
        if isValid:
            self.assigned(email).delete()
        raise Exception("That user is not on this jobsite")

    def isValid(self, email):
        test = list(map(str, User.objects.filter(email=email)))
        if test.length == 0:
            return False
        return True

    def addTool(self, tool):
        if not toolbox.validTool(tool):
            raise Exception("Tool does not exist")
        self.toolbox.add(tool)