from django import forms
from ToolOwnershipTracker.models import ToolReport, Tool, Toolbox, Jobsite, User, ToolType

class reportForm(forms.ModelForm):
    class Meta:
        model = ToolReport
        fields = {'tool', 'jobSite', 'toolbox','reportType','description'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.fields['toolbox'].queryset = Tool.objects.none()

        if 'jobSite' in self.data:
            try:
                jobsite_id = int(self.data.get('jobSite'))
                self.fields['toolbox'].queryset = Toolbox.objects.filter(jobsite_id=jobsite_id)
            except(ValueError, TypeError):
                pass
            
        elif self.instance.pk:
            self.fields['toolbox'].queryset = self.instance.jobsite.toolbox_set
        
        self.fields['tool'].queryset = Toolbox.objects.none()
        if 'toolbox' in self.data:
            try:
                toolbox_id = int(self.data.get('toolbox'))
                self.fields['tool'].queryset = Tool.objects.filter(toolbox_id=toolbox_id)
            except(ValueError, TypeError):
                pass
        
        elif self.instance.pk:
            self.fields['tool'].queryset = self.instance.toolbox.tool_set
