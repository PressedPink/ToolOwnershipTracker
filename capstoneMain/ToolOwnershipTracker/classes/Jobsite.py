from capstoneMain.ToolOwnershipTracker.classes.Users import User
from capstoneMain.ToolOwnershipTracker.classes import Toolbox
from capstoneMain.ToolOwnershipTracker.models import User, Toolbox, Jobsite, UserType, Tool


def Jobsite():
    def createJobsite(self, title, owner):
        if checkTitle(self, title):
            if isValid(self, owner):
                if isValidOwner(self, owner):
                    jobsite = Jobsite(owner=owner, title=title)
                    tbox = Toolbox.createToolbox(jobsite=jobsite)
                    jobsite.save()
                    tbox.save()
                    return True
                else:
                    raise Exception("This user cannot be the owner of a jobsite")
                    return False
            else:
                raise Exception("The owner is not a valid user")
                return False
        else:
            raise Exception("Name of Jobsite Cannot be left empty")
            return False

    def checkTitle(self, title):
        if title is None:
            return False
        return True

    def assignOwner(self, owner):
        if isValid(self, owner):
            if isValidOwner(self, owner):
                self.owner = owner
                self.save()
                return True
            else:
                raise Exception("This person cannot own a jobsite")
                return False
        else:
            raise Exception("This user does not exist")
            return False

    def addUser(self, user):
        if User.verifyEmailExists(self, user):
            if not self.assigned.contains(user):
                self.users.add(user)
                return True
            else:
                raise Exception("This user is already assigned this Jobsite")
                return False
        else:
            raise Exception("This user does not exist")
            return False

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

    def isInJobsite(self, email):
        if not self.assigned.contains(email):
            return False
        return True

    def removeUser(self, email):
        if isValid(self, email):
            if isInJobsite(self, email):
                self.assigned.remove(email)
                return True
            raise Exception("User is not in Jobsite")
            return False
        return False

    def isValid(self, email):
        test = list(map(str, User.objects.filter(email=email)))
        if test.length == 0:
            raise Exception("User does not exist")
            return False
        return True

    def isValidOwner(self, owner):
        if owner.role is 'U':
            return False
        return True
