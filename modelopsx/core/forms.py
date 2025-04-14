from django import forms
from .models import UseCase

class UseCaseForm(forms.ModelForm):
    class Meta:
        model = UseCase
        fields = ['name', 'gameplan', 'confluence_link', 'splunk_link', 'grafana_link', 'error_list_link']
        widgets = {
            'confluence_link': forms.URLInput(attrs={'readonly': True}),
            'splunk_link': forms.URLInput(attrs={'readonly': True}),
            'grafana_link': forms.URLInput(attrs={'readonly': True}),
            'error_list_link': forms.URLInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super(UseCaseForm, self).__init__(*args, **kwargs)
        # Make all except name and gameplan not required
        self.fields['confluence_link'].required = False
        self.fields['splunk_link'].required = False
        self.fields['grafana_link'].required = False
        self.fields['error_list_link'].required = False
