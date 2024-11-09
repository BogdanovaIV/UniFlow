from django import forms
from datetime import timedelta, datetime
from .models import (
    Term,
    StudyGroup,
    ScheduleTemplate,
    Subject,
    WeekdayChoices,
    Schedule,
    StudentMark)

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
        required=True,
        label="Term"
    )
    study_group = forms.ModelChoiceField(
        queryset=StudyGroup.active_objects(),
        required=True,
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


class ScheduleFilterForm(forms.Form):
    """
    A form to filter schedule based on selected dates and study group.

    Fields:
        - week (DateField): A date input field for selecting a week, used to
        filter data within the specified week period.
        - study_group: A ModelChoiceField that allows the user to select 
        a study group from the active study groups available in the database.
    """
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Week Date"
    )
    study_group = forms.ModelChoiceField(
        queryset=StudyGroup.active_objects(),
        required=True,
        label="Study Group"
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the ScheduleFilterForm with optional customization for
        students.

        Args:
            is_student (bool, optional): Indicates if the form is being used by
            a student. Defaults to False. When True, the 'study_group' field is 
            pre-filled with the student's study group and made read-only.
            user_study_group (str, optional): The study group assigned to the 
            student user, if applicable. Defaults to an empty string.

        """
        is_student = kwargs.pop('is_student', False)
        user_study_group = kwargs.pop('user_study_group', '')
        super().__init__(*args, **kwargs)
        if is_student:
            self.fields['study_group'].initial = user_study_group
            self.fields['study_group'].disabled = True

    def get_filter_params(self):
        """
        Generates a dictionary of filtering parameters based on the form inputs.
        
        The week start date is extended to a full week range (Monday to Sunday), 
        allowing the schedule data to be filtered by the chosen study group 
        and date range.
        
        Returns:
            dict: Filter parameters including study group and date range for
            the selected week.
        """
        week_start = None
        week_end = None
        study_group = None
        if self.is_valid():
            
            week_start = (
                self.cleaned_data.get('date')
                if 'date' in self.cleaned_data else None
            )
            study_group = (
                self.cleaned_data.get('study_group')
                if 'study_group' in self.cleaned_data else None
            )
            if week_start:
                week_start = week_start - timedelta(days=week_start.weekday())
                week_end = week_start + timedelta(days=6)

        return {
                'study_group': study_group,
                'date__range': (week_start, week_end)
            }


class ScheduleForm(forms.ModelForm):
    """
    A form for editing Schedule instances with restricted field access.
    
    - Fields 'date', 'study_group', and 'order_number' are disabled,
    leaving only 'homework' editable when an instance exists.
    - Filters 'homework' to display only active subjects.
    """
    date_str = forms.CharField(
        label='Date (str)',
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
    weekday_value = forms.IntegerField(
        label='Weekday (value)',
        required=False,
        widget=forms.NumberInput()
    )

    class Meta:
        model = Schedule
        fields = [
            'date',
            'study_group',
            'order_number',
            'subject',
            'homework',
            'study_group_name',
            'weekday_name',
            'weekday_value',
            'date_str'
        ]

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting specific fields to read-only and limiting
        'subject' choices to active subjects.
        """
        super().__init__(*args, **kwargs)

        weekday_value = None
        if self.instance and self.instance.pk:
            self.fields['date_str'].initial = str(self.instance.date)
            self.fields['study_group_name'].initial = self.instance.study_group
            self.fields['weekday_name'].initial = (
                WeekdayChoices(self.instance.date.weekday()).label
            )
            self.fields['weekday_value'].initial = self.instance.date.weekday()

        if 'study_group' in self.initial and self.initial['study_group']:
            self.fields['study_group_name'].initial = (
                StudyGroup.objects.get(pk=self.initial['study_group'])
            )
        if 'date' in self.initial and self.initial['date']:
            date_obj = (
                datetime.strptime(self.initial['date'], "%Y-%m-%d").date()
                if isinstance(self.initial['date'], str)
                else self.initial['date']
            )
            self.fields['date_str'].initial = str(self.initial['date'])
            self.fields['weekday_name'].initial = (
                WeekdayChoices(date_obj.weekday()).label
            )
            self.fields['weekday_value'].initial = (
                date_obj.weekday()
            )
        self.fields['subject'].queryset = Subject.active_objects()


class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ['student', 'mark']