from capstoneMain.ToolOwnershipTracker.Users import User


def Jobsite():
    def createJobsite(self, title, owner):
        checkTitle(self, title)
        checkOwner(self, owner)
        jobsite = Jobsite(title, owner)
        jobsite.save()

    def checkTitle(self, title):
        if title is None:
            raise Exception("Name of Jobsite Cannot be left empty")
        return True

    def checkOwner(self, owner):
        test = list(map(str, User.objects.filter(email=owner)))
        if test.length == 0:
            raise Exception("User does not exist")
