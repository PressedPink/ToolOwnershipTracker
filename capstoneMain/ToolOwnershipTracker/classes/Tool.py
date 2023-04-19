from ToolOwnershipTracker.classes.Users import UserClass
from ToolOwnershipTracker.classes.Toolbox import ToolboxClass
from ToolOwnershipTracker.models import Jobsite, Toolbox, Tool


class ToolClass:
    def createTool(self):
        tool = Tool()
        tool.save()
        return True

    def isValidName(self, name):
        if name is None:
            return False
        return True

    def assignToolName(self, toolID, name):
        if ToolClass.isValidName(self, name):
            if ToolClass.isValidTool(self, toolID):
                tool = Tool.objects.get(id = toolID)
                tool.name = name
                tool.save()
            else:
                raise Exception("Tool does not exist!")
        else:
            raise Exception("Name of tool cannot be left empty!")
        
    def isValidTool(self, toolID):
        test = list(map(str, Tool.objects.filter(id = toolID)))
        if len(test) == 0:
            return False
        else:
            return True

    def isValidToolbox(self, toolboxID):
        test = list(map(str, Toolbox.objects.filter(id = toolboxID)))
        if len(test) == 0:
            return False
        else:
            return True

    def toolAlreadyExists(self, name, toolboxID):
        toolbox = Tool.objects.get(id = toolboxID)
        test = list(map(str, Tool.objects.filter(name=name, toolbox = toolbox)))
        if len(test) == 0:
            return False
        else:
            return True

    def addToToolbox(self, toolID, toolboxID):
        if ToolClass.isValidTool(self, toolID):
            if ToolClass.isValidToolbox(self, toolboxID):
                if not ToolClass.containedInThisToolbox(self, toolID, toolboxID):
                    if not ToolClass.containedInAnyToolbox(self, toolID):
                        tool = Tool.objects.get(id = toolID)
                        toolbox = Toolbox.objects.get(id = toolboxID)
                        tool.toolbox = toolbox
                        tool.save()
                        return True
                    else:
                        raise Exception("Tool is already contained in another toolbox!")
                else:
                    raise Exception("Tool is already assigned to this toolbox")
            else:
                raise Exception("Toolbox does not exist!")
        else:
            raise Exception("Tool does not exist!")

    def removeFromToolbox(self, toolID, toolboxID):
        if ToolClass.isValidTool(self, toolID):
            if ToolClass.isValidToolbox(self, toolboxID):
                if ToolClass.containedInThisToolbox(self, toolID, toolboxID):
                    tool = Tool.objects.get(id = toolID)
                    tool.toolbox = None
                    tool.save()
                    return True
                else:
                    raise Exception("Tool is not contained in this toolbox!")
            else:
                raise Exception("Toolbox does not exist!")
        else:
            raise Exception("Tool does not exist!")

    def containedInThisToolbox(self, toolID, toolboxID):
        if ToolClass.isValidTool(self, toolID):
            if ToolClass.isValidToolbox(self, toolboxID):
                tool = Tool.objects.get(id = toolID)
                toolbox = Toolbox.objects.get(id = toolboxID)
                if tool.toolbox == toolbox:
                    return True
                else:
                    return False
            else:
                raise Exception("Toolbox does not exist!")
        else:
            raise Exception("Tool does not exist!")

    def containedInAnyToolbox(self, toolID):
        if ToolClass.isValidTool(self, toolID):
            tool = Tool.objects.get(id = toolID)
            if tool.toolbox != None:
                return True
            else:
                return False

    def deleteTool(self, toolID):
        if not ToolClass.containedInAnyToolbox(self, toolID):
            tool = Tool.objects.get(id = toolID)
            tool.delete()
            return True
        else:
            raise Exception("Tool must be returned from toolbox before tool removal!")