from capstoneMain.ToolOwnershipTracker.Jobsite import Jobsite


def Toolbox():
    def createToolbox(self, id, owner):
        isValidJobsite(id)
        Jobsite.isValid(owner)
        tbx = Toolbox(self, id, owner)
        tbx.save()
        return True


    def isValidJobsite(self, id):
        test = list(map(str, Jobsite.objects.filter(id=id)))
        if test.length == 0:
            return False
        return True
