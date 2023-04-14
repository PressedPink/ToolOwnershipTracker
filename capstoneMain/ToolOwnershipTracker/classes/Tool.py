from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.models import Jobsite, Toolbox, Tool


class ToolClass:
    def createTool(self):
        tool = Tool()
        tool.save()
        return True

    def deleteTool(self):
        if ToolClass.isUnassigned():
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

    def addToolToUserToolbox(self, toolID, toolboxID):
        try:
            toolbox = Toolbox.objects.get(id=toolboxID)
            tool = Tool.objects.get(id=toolID)
            
            
        except Toolbox.DoesNotExist:
            raise Exception("Toolbox does not exist!")
        if Tool.isUnassigned(self, toolID):
            self.tools.add(tool)

    # adds removes tool from toolbox if it is in the toolbox and it is not assigned to a user
    def removeToolFromUserToolbox(self, tool):
        if self.tools.contains(tool) and not User.verifyEmailExists(self, tool.toolbox):
            self.remove.tools(tool)

    def addToolToJobsiteToolbox(self, tool):
        test = list(map(str, Tool.objects.filter(id=tool)))
        if test.length == 0:
            raise Exception("Tool does not exist")
            return False
        Tool.changeUser(tool, self.id)
        self.tools.add(tool)
        return True

    def removeToolFromJobsiteToolbox(self, toolID, toolboxID):
        if ToolClass.containedInToolbox(self, toolID, toolboxID):

            if tool.toolbox is None or tool.toolbox is self.id:
                self.toolbox.remove(tool)
                Tool.unassignToolbox(tool)
            else:
                raise Exception("This is assigned to a user")
                return False
        else:
            raise Exception("Tool is not in toolbox!")
            return False
        return True

    def containedInToolbox(self, toolID, toolboxID):
        pass
