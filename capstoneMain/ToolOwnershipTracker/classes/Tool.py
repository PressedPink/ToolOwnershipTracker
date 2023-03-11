from capstoneMain.ToolOwnershipTracker.Users import User

def Tool():

    def createTool(self):
        tool = Tool(self)
        tool.save()

    def deleteTool():

    def isUnassigned(self, owner, jobsite):
        if owner is not None:
            raise Exception("This tool is already assigned to a User")
        if jobsite is not None:
            raise Exception("This tool is already in another jobsite's toolbox")
        return True

    def changeUser(self, owner):
        unassignToolUser(self)
        self.owner=owner
        self.save()


    def unassignToolUser(self):
        self.remove.owner()
        self.save()

    def unassignToolJobsite(self):
        self.remove.jobsite()
        self.save()

    def changeLocation(self,owner, jobsite):
        unassignToolJobsite(self)
        isUnassigned(self,owner,jobsite)
        self.jobsite=jobsite
        self.save()