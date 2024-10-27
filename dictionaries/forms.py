from django import forms
from .models import Term, StudyGroup, ScheduleTemplate, Subject  

class ScheduleTemplateFilterForm(forms.Form):
    """
    A form to filter schedule templates based on selected term and study group.

    Fields:
        - term: A ModelChoiceField that allows the user to select a term 
          from the active terms available in the database.
        - study_group: A ModelChoiceField that allows the user to select 
          a study group from the active study groups available in the database.
    """
    term = forms.ModelChoiceField(
        queryset=Term.active_objects(),
        label="Term"
    )
    study_group = forms.ModelChoiceField(
        queryset=StudyGroup.active_objects(),
        label="Study Group"
    )

class ScheduleTemplateForm(forms.ModelForm):
    """
    A form for editing ScheduleTemplate instances with restricted field access.
    
    - Fields 'term', 'study_group', 'weekday', and 'order_number' are disabled,
    leaving only 'subject' editable when an instance exists.
    - Filters 'subject' to display only active subjects.
    """
    class Meta:
        model = ScheduleTemplate
        fields = ['term', 'study_group', 'weekday', 'order_number', 'subject']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting specific fields to read-only and limiting
        'subject' choices to active subjects.
        """
        super().__init__(*args, **kwargs)
        
        self.fields['term'].disabled = True
        self.fields['study_group'].disabled = True
        self.fields['weekday'].disabled = True
        self.fields['order_number'].disabled = True
        self.fields['subject'].queryset = Subject.active_objects()