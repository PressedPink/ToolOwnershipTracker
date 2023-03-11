from capstoneMain.ToolOwnershipTracker.Jobsite import Jobsite




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
        isUnassigned(self,tool)

    def removeTool(self,tool):
        isUnassigned(self,tool)
        self.remove.tools(tool)
        Tool.remove.toolbox()

    def isUnassigned(self, tool):
        if tool.owner is not None:
            raise Exception("This tool is already assigned to a User")
        if tool.jobsite is not None:
            raise Exception("This tool is already in another jobsite's toolbox")
        return True


