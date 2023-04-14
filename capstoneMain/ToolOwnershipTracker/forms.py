from django import forms
from ToolOwnershipTracker.models import ToolReport, Tool, Toolbox, Jobsite, User, ToolType
from django.forms import ModelForm, Textarea, TextInput

class ReportForm(forms.ModelForm):
    class Meta:
        model = ToolReport
        fields = ('reportType','jobsite', 'toolbox', 'tool', 'topic','description')
        widgets = {
          'description': Textarea(attrs={'size':'20'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['size'] = 20
        self.fields['toolbox'].queryset = Toolbox.objects.none()

        if 'jobsite' in self.data:
            try:
                jobsite_id = int(self.data.get('jobsite'))
                self.fields['toolbox'].queryset = Toolbox.objects.filter(jobsite_id=jobsite_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Toolbox queryset
        elif self.instance.pk:
            self.fields['toolbox'].queryset = self.instance.jobsite.toolbox_set.order_by('name')

        self.fields['tool'].queryset = Tool.objects.none()
        if 'toolbox' in self.data:
            try:
                toolbox_id = int(self.data.get('toolbox'))
                self.fields['tool'].queryset = Tool.objects.filter(toolbox_id=toolbox_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Toolbox queryset
        elif self.instance.pk:
            self.fields['tool'].queryset = self.instance.toolbox.tool.order_by('name')

