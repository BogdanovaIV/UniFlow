from django import forms
from .models import Term, StudyGroup

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