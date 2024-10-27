from django import forms
from .models import Term, StudyGroup, ScheduleTemplate, Subject, WeekdayChoices  

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
    term_name = forms.CharField(
        label='Term',
        required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    study_group_name = forms.CharField(
        label='Study group',
        required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    weekday_name = forms.CharField(
        label='Weekday',
        required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    class Meta:
        model = ScheduleTemplate
        fields = [
            'term',
            'study_group',
            'weekday',
            'order_number',
            'subject',
            'term_name',
            'study_group_name',
            'weekday_name'
        ]

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting specific fields to read-only and limiting
        'subject' choices to active subjects.
        """
        super().__init__(*args, **kwargs)
        self.fields['term'].disabled = True
        self.fields['study_group'].disabled = True
        self.fields['weekday'].disabled = True

        weekday_value = None
        if self.instance and self.instance.pk:
            self.fields['term_name'].initial = self.instance.term
            self.fields['study_group_name'].initial = self.instance.study_group
            weekday_value = self.instance.weekday

        if 'term' in self.initial:
            self.fields['term_name'].initial = Term.objects.get(
                pk=self.initial['term']
            )

        if 'study_group' in self.initial:
            self.fields['study_group_name'].initial = StudyGroup.objects.get(
                pk=self.initial['study_group']
        )

        if 'weekday' in self.initial:
            weekday_value = int(self.initial['weekday'])

        if weekday_value is not None:
            self.fields['weekday_name'].initial = WeekdayChoices(weekday_value).label
        self.fields['subject'].queryset = Subject.active_objects()