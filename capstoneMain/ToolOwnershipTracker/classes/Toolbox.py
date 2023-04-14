from ToolOwnershipTracker.models import User, Toolbox, Jobsite
from ToolOwnershipTracker.classes.Users import UserClass

class ToolboxClass:
    def createUserToolbox(self, email):
        if UserClass.verifyEmailExists(email):
            if ToolboxClass.checkUserToolboxDoesNotExist(email):
                toolboxOwner = User.objects.get(email = email)
                newToolbox = Toolbox(owner=toolboxOwner, jobsite = None)
                newToolbox.save()
            else:
                raise Exception("User toolbox already exists!")
        else:
            raise Exception("User does not exist!")
        
    def createJobsiteToolbox(self, email, jobsiteID):
        if ToolboxClass.isValidJobsite(jobsiteID):
            if ToolboxClass.checkJobsiteToolboxDoesNotExist(jobsiteID):
                jobsiteOwner = User.objects.get(email = email)
                jobsite = Jobsite.objects.get(id = jobsiteID)
                newToolbox = Toolbox(owner = jobsiteOwner, jobsite = jobsite)
                newToolbox.save()
            else:
                raise Exception("Jobsite toolbox already exists!")
        else:
            raise Exception("Jobsite does not exist!")


    def isValidJobsite(self, jobsiteID):
        test = list(map(str, Jobsite.objects.filter(id = jobsiteID)))
        if len(test) == 0:
            return False
        return True
    
    def isEmpty(self, toolboxID):
        try:
            toolbox = Toolbox.objects.get(id=toolboxID)
            return not toolbox.tool_set.exists()
        except Toolbox.DoesNotExist:
            raise Exception("Toolbox does not exist!")

    def checkUserToolboxDoesNotExist(email):
        user = User.objects.get(email = email)
        test = list(map(str, Toolbox.objects.filter(owner = user, jobsite = None)))
        if len(test) == 0:
            return True
        else:
            return False

    def checkJobsiteToolboxDoesNotExist(jobsiteID):
        test = list(map(str, Toolbox.objects.filter(id = jobsiteID)))
        if len(test) == 0:
            return True
        else:
            return False