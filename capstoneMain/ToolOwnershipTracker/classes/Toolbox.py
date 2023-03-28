from models import Jobsite, Tool



def Toolbox():
    def createToolbox(self, ToolboxID, owner):
        isValidJobsite(ToolboxID)
        Jobsite.isValid(owner)
        tbx = Toolbox(self, ToolboxID, owner)
        tbx.save()
        return True

    def isValidJobsite(self, ToolboxID):
        test = list(map(str, Jobsite.objects.filter(id=id)))
        if test.length == 0:
            return False
        return True

    def addTool(self, tool):
        Tool.isUnassigned(self, tool)
        self.tools.add(tool)

    def removeTool(self, tool):
        Tool.isUnassigned(self, tool)
        self.remove.tools(tool)
        Tool.remove.toolbox()
