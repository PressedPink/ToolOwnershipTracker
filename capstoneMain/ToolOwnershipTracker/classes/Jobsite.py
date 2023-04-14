from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.models import User, Toolbox, Jobsite
import uuid


class JobsiteClass:
    def createJobsite(self, title, email):
        if JobsiteClass.isValidTitle(self, title):
            if UserClass.verifyEmailExists(self, email):
                if JobsiteClass.isValidOwner(self, email):
                    if not JobsiteClass.jobsiteAlreadyExists(self, title, email):
                        jobsiteOwner = User.objects.get(email=email)
                        jobsite = Jobsite(owner=jobsiteOwner, title=title)
                        jobsite.save()
                        ToolboxClass.createJobsiteToolbox(self=self, email=email, jobsiteID=jobsite.id)
                        
                        return True
                    else:
                        raise Exception("Jobsite already exists!")
                else:
                    raise Exception("Jobsite owner must be of type supervisor or administrator!")
            else:
                raise Exception("User does not exist!")
        else:
            raise Exception("Name of jobsite cannot be left empty")

    def isValidTitle(self, title):
        if title is None:
            return False
        return True
    
    def assignTitle(self, jobsiteID, title):
        if JobsiteClass.isValidTitle(self, title):
            if JobsiteClass.isValidJobsite(self, jobsiteID):
                jobsite = Jobsite.objects.get(id = jobsiteID)
                jobsite.title = title
                jobsite.save()
            else:
                raise Exception("Jobsite does not exist!")
        else:
            raise Exception("Name of jobsite cannot be left empty")

    def isValidOwner(self, email):
        user = User.objects.get(email=email)
        if user.role == 'U':
            return False
        return True

    def assignOwner(self, jobsiteID, email):
        if JobsiteClass.isValidOwner(self, email):
            if JobsiteClass.isValidJobsite(self, jobsiteID):
                jobsiteOwner = User.objects.get(email=email)
                jobsite = Jobsite.objects.get(id = jobsiteID)
                jobsite.owner = jobsiteOwner
                jobsite.save()
                return True
            else:
                raise Exception("Jobsite does not exist!")
        else:
            raise Exception("User does not exist!")
    
    def isValidJobsite(self, jobsiteID):
        test = list(map(str, Jobsite.objects.filter(id = jobsiteID)))
        if len(test) == 0:
            return False
        else:
            return True

    def addUser(self, jobsiteID, email):
        if UserClass.verifyEmailExists(self, email):
            if JobsiteClass.isValidJobsite(self, jobsiteID):
                if not JobsiteClass.containsUser(self, jobsiteID, email):
                    user = User.objects.get(email=email)
                    jobsite = Jobsite.objects.get(id = jobsiteID)
                    jobsite.assigned.add(user)
                    jobsite.save()
                    return True
                else:
                    raise Exception("User is already assigned to this jobsite!")
            else:
                raise Exception("Jobsite does not exist!")
        else:
            raise Exception("User does not exist!")

    def removeJobsite(self, jobsiteID):
        jobsite = Jobsite.objects.get(id = jobsiteID)
        toolbox = Toolbox.objects.get(jobsite = jobsite)
        if ToolboxClass.isEmpty(self, toolbox.id):
            jobsite.delete()
            return True
        else:
            raise Exception("Jobsite toolbox must be empty before jobsite removal!")

    def removeUser(self, jobsiteID, email):
        if UserClass.verifyEmailExists(self, email):
            if JobsiteClass.isValidJobsite(self, jobsiteID):
                if JobsiteClass.containsUser(self, jobsiteID, email):
                    jobsite = Jobsite.objects.get(id = jobsiteID)
                    user = User.objects.get(email = email)
                    jobsite.assigned.remove(user)
                    jobsite.save()
                    return True
                else:
                    raise Exception("User not assigned to jobsite!")
            else:
                raise Exception("Jobsite does not exist!")
        else:
            raise Exception("User does not exist!")

    def containsUser(self, jobsiteID, email):
        if UserClass.verifyEmailExists(self, email):
            if JobsiteClass.isValidJobsite(self, jobsiteID):
                jobsite = Jobsite.objects.get(id = jobsiteID)
                user = User.objects.get(email = email)
                if jobsite.assigned.filter(User = user).exists():
                    return True
                else:
                    return False
            else:
                raise Exception("Jobsite does not exist!")
        else:
            raise Exception("User does not exist!")
        
    def jobsiteAlreadyExists(self, title, email):
        user = User.objects.get(email = email)
        test = list(map(str, Jobsite.objects.filter(title = title, owner = user)))
        if len(test) == 0:
            return False
        else:
            return True