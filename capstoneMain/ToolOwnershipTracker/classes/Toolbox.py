from ToolOwnershipTracker.classes.Tool import Tool
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


    def isValidJobsite(jobsiteID):
        test = list(map(str, Jobsite.objects.filter(id = jobsiteID)))
        if len(test) == 0:
            return False
        return True
    
    def isEmpty(jobsite):
        pass


    # adds tool to toolbox if it does not belong somewhere
    def addTool(self, tool):
        if Tool.isUnassigned(self, tool):
            self.tools.add(tool)

    # adds removes tool from toolbox if it is in the toolbox and it is not assigned to a user
    def removeTool(self, tool):
        if self.tools.contains(tool) and not User.verifyEmailExists(self, tool.toolbox):
            self.remove.tools(tool)

    def addTool(self, tool):
        test = list(map(str, Tool.objects.filter(id=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        Tool.changeUser(tool, self.id)
        self.tools.add(tool)
        return True

    def removeTool(self, tool):
        if ToolboxClass.containsTool(self, tool):
            if tool.toolbox is None or tool.toolbox is self.id:
                self.toolbox.remove(tool)
                Tool.unassignToolbox(tool)
            else:
                raise Exception("This is assigned to a user")
                return False
        else:
            raise Exception("Tool is not in toolbox")
            return False
        return True

    def containsTool(self, tool):
        if not self.tools.contains(tool):
            return False
        return True

    # removes all tools from jobsite's toolbox
    def removeAllTools(self):
        for tools in self.toolbox.tools:
            if not ToolboxClass.removeTool(self, self.tool):
                raise Exception("Unable to remove" + tools.id)
                return False
        return True

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