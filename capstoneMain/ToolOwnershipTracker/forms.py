from django import forms
from ToolOwnershipTracker.models import ToolReport, Tool, Toolbox, Jobsite, User, ToolType
from django.forms import ModelForm, Textarea, TextInput
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReportForm(forms.ModelForm):
    class Meta:
        model = ToolReport
        fields = ('reportType', 'reporter', 'toolbox', 'tool', 'topic', 'created', 'time', 'description')
        widgets = {
          'description': Textarea(attrs={'size':'20'}),
          'created': DateInput(),
          'time': TimeInput(),
          'reporter': forms.HiddenInput(),
          'toolbox': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.reporter = kwargs.pop('reporter')
        self.toolbox = kwargs.pop('toolbox')
        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields['reporter'].initial = self.reporter
        self.fields['toolbox'].initial = self.toolbox
        self.fields['created'].initial = datetime.now()
        self.fields['time'].initial = datetime.now()

        self.fields['description'].widget.attrs['size'] = 20
        self.fields['tool'].queryset = Tool.objects.filter(toolbox = self.toolbox)







