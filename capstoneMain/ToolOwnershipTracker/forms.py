from django import forms
from ToolOwnershipTracker.models import ToolReport, Tool, Toolbox, Jobsite, User, ToolType
from django.forms import ModelForm, Textarea, TextInput
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReportForm(forms.ModelForm):
    class Meta:
        model = ToolReport
        fields = ('reportType','reporter', 'jobsite', 'toolbox', 'tool', 'topic', 'created', 'description')
        widgets = {
          'description': Textarea(attrs={'size':'20'}),
          'created': DateInput()
        }
    def __init__(self, *args, **kwargs):
        self.reporter = kwargs.pop('reporter')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['reporter'].queryset = User.objects.filter(
            email=self.reporter)
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
            self.fields['tool'].queryset = Tool.objects.all()

