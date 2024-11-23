from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from dictionaries.forms import ScheduleFilterForm, ScheduleForm
from dictionaries.models import (
    Schedule,
    WeekdayChoices,
    ScheduleTemplate,
    StudyGroup,
    Term,
    StudentMark
    )

from users.context_processors import user_profile_parameters
from users.models import UserProfile


class ScheduleBaseView(PermissionRequiredMixin, View):
    """
    Base view for handling common functionality across schedule views, such as
    form data handling and redirection.

    This view provides shared utilities for schedule views in the tutor
    dashboard, enabling form data initialization, date parsing, and
    standardized redirection upon form submission.
    """
    template_name = 'tutor_dashboard/edit_schedule.html'

    def parse_date(self, date_request):
        """
        Parses a date string into a date object.

        Parameters:
        - date_request: A date string in 'YYYY-MM-DD' format or a date object.

        Returns:
        - A date object if the input is a valid date string, or the original
        input if it's already a date.
        """
        if isinstance(date_request, str) and date_request:
            # Convert the date string to a date object
            parsed_date = datetime.strptime(date_request, "%Y-%m-%d").date()
        else:
            parsed_date = date_request

        return parsed_date

    def get_initial_data(self, request):
        """
        Extracts initial data from the request for form pre-population.

        Parameters:
        - request: The HTTP request object containing GET or POST data.

        Returns:
        - A dictionary containing initial values for form fields: 'date',
        'study_group', 'order_number', and 'subject'.
        """
        def get_first_value(key):
            """Retrieve the first value for a given key from the request."""
            values = request.getlist(key)
            return values[0] if values else request.get(key)

        return {
            'date': self.parse_date(get_first_value('date')),
            'study_group': get_first_value('study_group'),
            'order_number': get_first_value('order_number'),
            'subject': get_first_value('subject'),
        }

    def handle_redirect(self, form):
        """
        Redirects to the schedule view with the specified date and study group
        parameters.

        Parameters:
        - form: A dictionary containing form data, where 'date' and
        'study_group' are expected keys. 'study_group' can be an instance
        of `StudyGroup` or a string ID.

        Returns:
        - A HttpResponseRedirect to the 'tutor:schedule' URL, including query
        parameters for date and study group.
        """
        date = form.get('date') if 'date' in form else ''
        study_group = (
            form.get('study_group').id
            if isinstance(form.get('study_group'), StudyGroup)
            else form.get('study_group')
        ) if 'study_group' in form else ''

        return redirect(
            f"{reverse('tutor:schedule')}?date={date}"
            f"&study_group={study_group}",
        )


class ScheduleView(PermissionRequiredMixin, View):
    """
    View for displaying and filtering the schedule based on user-selected term
    and study group.

    This view provides functionality for displaying a filtered schedule based
    on the selected term and study group, organizing schedule data by weekdays,
    and handling both GET and POST requests for schedule filtering.
    """
    template_name = 'tutor_dashboard/schedule.html'
    url_name = 'tutor:schedule'
    permission_required = 'dictionaries.view_schedule'

    def get(self, request):
        """
        Handles GET requests to display the schedule with the filter form.

        Parameters:
        - request: The HTTP request object containing optional query parameters
        for date and study group.

        Returns:
        - Renders the schedule page with the filter form and displays the
        filtered schedule if valid.
        Shows error messages if form validation fails and displays an info
        message if no schedule matches the filter.
        """
        user_profile_context = user_profile_parameters(request)
        context_var = {
            'user': request.user,
            **user_profile_context
        }
        get_params = request.GET

        date = get_params.get('date') if 'date' in get_params else ''
        if context_var['is_student']:
            get_params = request.GET.copy()
            get_params['study_group'] = context_var['user_study_group']

        study_group_id = (
            get_params.get('study_group') if 'study_group' in get_params
            else ''
        )

        if not date:
            if isinstance(get_params, dict):
                get_params = request.GET.copy()
            date = datetime.now()
            get_params['date'] = date

        form = ScheduleFilterForm(
            get_params,
            is_student=context_var['is_student'],
            user_study_group=context_var['user_study_group'],
        )

        filter_params = form.get_filter_params()
        schedule, table_empty = self.get_schedule(
            filter_params, context_var
        )
        if table_empty and len(get_params) == 2:
            # Display message if no schedule is available for the selected
            # filters
            messages.info(
                request,
                "No schedule available for the selected date and study group."
            )
        elif len(get_params) == 2:
            # Display success message when schedule is successfully filtered
            messages.success(request, "Schedule displayed successfully.")

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'schedule': schedule,
                'table_empty': table_empty,
                'selection_valid': form.is_valid()
            }
        )

    def post(self, request):
        """
        Handles POST requests to process the schedule filter form submission.

        Parameters:
        - request: The HTTP request object containing POST data with date and
        study group.

        Returns:
        - Redirects to the schedule view with selected date and study group as
        query parameters.
        """
        user_profile_context = user_profile_parameters(request)
        context_var = {
            'user': request.user,
            **user_profile_context
        }
        form = ScheduleFilterForm(
            request.POST,
            is_student=context_var['is_student'],
            user_study_group=context_var['user_study_group'],
        )

        date = request.POST.get('date') if 'date' in request.POST else ''
        study_group = (
            request.POST.get('study_group') if 'study_group' in request.POST
            else ''
        )
        if context_var['is_student']:
            return redirect(f"{reverse(self.url_name)}?date={date}")
        else:
            return redirect(
                f"{reverse(self.url_name)}?date={date}"
                f"&study_group={study_group}"
            )

    def get_schedule(self, filter_params, context_var):
        """
        Retrieves and organizes the schedule based on selected date range and
        study group.

        Parameters:
        - filter_params: Dictionary containing filter parameters for date range
        and study group.
        - context_var: context processor variables (user, user_study_group...).

        Returns:
        - A tuple with:
        1. Organized schedule dictionary by weekdays, where each weekday
        contains details for subjects and homework.
        2. Boolean indicating whether the schedule table is empty (no schedule
        found for the filters).
        """
        if filter_params['date__range'][0] and filter_params['study_group']:
            objects = Schedule.objects.filter(**filter_params)
            table_empty = not objects.exists()
        else:
            objects = Schedule.objects.none()
            table_empty = True

        return (
            self.get_full_week_schedule(objects, filter_params, context_var),
            table_empty
        )

    def get_full_week_schedule(self, objects, filter_params, context_var):
        """
        Organizes schedule objects by weekdays within the selected date range.

        Parameters:
        - objects: Queryset of Schedule objects filtered by the selected term
        and study group.
        - filter_params: Dictionary of filter parameters, specifically date
        range and study group.
        - context_var: context processor variables (user, user_study_group...).

        Returns:
        - A dictionary representing the weekly schedule, where each day
        includes its date, weekday label, and details for each order number
        (up to 10), such as subject, homework assignments and the number of
        student marks.
        """
        schedule = {
            value: {
                'label_weekday': label,
                'date': filter_params['date__range'][0] + timedelta(
                    days=(value)
                    )
                if filter_params['date__range'][0] else '',
                'date_str': str(
                    filter_params['date__range'][0] + timedelta(days=(value))
                    ) if filter_params['date__range'][0] else '',
                'details': {order: {
                    'id': '',
                    'subject': '',
                    'homework': '',
                    'marks': 0
                    } for order in range(1, 11)}
            }
            for value, label in WeekdayChoices.choices
        }
        for object in objects:
            marks = 0
            if context_var['is_student']:
                student_marks = StudentMark.objects.filter(
                    schedule=object, student=context_var['user'])
                if student_marks.exists():
                    marks = student_marks.first().mark
            else:
                marks = StudentMark.objects.filter(schedule=object).count()

            schedule[object.date.weekday()]['details'][object.order_number] = {
                'id': object.id,
                'subject': object.subject,
                'homework': 'Tasks: ' + object.homework,
                'marks': marks,
            }
        return schedule


class EditScheduleView(ScheduleBaseView):
    """
    View to edit an existing Schedule entry.

    This view allows users with the necessary permissions to edit an existing
    Schedule instance. It provides methods to handle both GET requests, which
    render the form with the current Schedule data, and POST requests, which
    update the Schedule with the submitted form data.
    """
    permission_required = 'dictionaries.change_schedule'

    def get(self, request, pk):
        """
        Renders the form with the existing Schedule instance for editing.

        Parameters:
        - request: The HTTP request object containing request data.
        - pk: Primary key of the Schedule instance to be edited.

        Returns:
        - Renders the `edit_schedule.html` template with:
        1. `schedule`: The form pre-filled with the current Schedule data.
        2. `student_marks`: A queryset of StudentMark instances related to the
        schedule.
        3. `users`: A queryset of UserProfile instances in the study group for
        the schedule.
        """
        schedule = Schedule.objects.get(pk=pk)
        form = ScheduleForm(instance=schedule)
        student_marks = StudentMark.objects.filter(schedule=schedule)
        users = UserProfile.objects.filter(
            study_group=schedule.study_group
            ).select_related('user')

        return render(
            request,
            self.template_name,
            {
                'schedule': form,
                'student_marks': student_marks,
                'users': users,
            }
        )

    def post(self, request, pk):
        """
        Saves the updated Schedule instance or reloads the form on error.

        Parameters:
        - request: The HTTP request object containing POST data.
        - pk: Primary key of the Schedule instance to be updated.

        Returns:
        - If the form is valid: Saves the Schedule and redirects to the
        schedule view with success message.
        - If the form is invalid: Reloads the form with error messages
        displayed for each invalid field.
        """
        schedule = get_object_or_404(Schedule, pk=pk)
        form = ScheduleForm(request.POST, instance=schedule)

        if form.is_valid():
            form.save()
            data = {
                'date': form.cleaned_data.get('date'),
                'study_group': form.cleaned_data.get('study_group'),
            }
            messages.success(request, "Schedule updated successfully.")
            return self.handle_redirect(data)

        # Form validation error message
        for field, errors in form.errors.items():
            messages.error(request, f"Error in {field}: {', '.join(errors)}")

        return render(request, self.template_name, {'form': form})


class AddScheduleView(ScheduleBaseView):
    """
    View to add a new Schedule entry.

    This view allows users with the necessary permissions to create a new
    Schedule. It uses initial data extracted from query parameters to pre-fill
    the form fields. Handles both GET requests, which display the form, and
    POST requests, which process the form submission.
    """
    permission_required = 'dictionaries.add_schedule'

    def get(self, request):
        """
        Renders the form to add a new Schedule, pre-filled with initial data if
        available.

        Parameters:
        - request: The HTTP request object containing GET data.

        Returns:
        - Renders the `edit_schedule.html` template with:
        1. `schedule`: The form instance, pre-filled with initial data based on
        query parameters.
        """
        initial_data = self.get_initial_data(request.GET)
        form = ScheduleForm(initial=initial_data)

        return render(request, self.template_name, {'schedule': form})

    def post(self, request):
        """
        Processes the form submission to add a new Schedule entry.

        Parameters:
        - request: The HTTP request object containing POST data.

        Returns:
        - If the form is valid: Saves the new Schedule instance and redirects
        to the edit schedule page with a success message.
        - If the form is invalid: Reloads the form with error messages
        displayed for each invalid field.
        """

        initial_data = self.get_initial_data(request.POST)
        form = ScheduleForm(request.POST, initial=initial_data)

        if form.is_valid():
            schedule = form.save()
            messages.success(request, "Schedule added successfully.")
            return redirect(
                reverse('tutor:edit_schedule', args=[schedule.pk])
            )

        # Form validation error message
        for field, errors in form.errors.items():
            messages.error(request, f"Error in {field}: {', '.join(errors)}")

        return render(request, self.template_name, {'form': form})


class DeleteScheduleView(ScheduleBaseView):
    """
    View to delete an existing Schedule entry.

    This view allows users with the appropriate permissions to delete a
    Schedule. It handles POST requests to delete the specified Schedule
    instance and provides feedback messages based on the outcome.
    """
    permission_required = 'dictionaries.delete_schedule'

    def post(self, request, pk):
        """
        Processes the deletion of a specified Schedule entry.

        Parameters:
        - request: The HTTP request object containing POST data.
        - pk: Primary key of the Schedule to be deleted.

        Returns:
        - Redirects to the schedule list page with filter parameters for date
        and study group, if the deletion is successful.
        """
        schedule = get_object_or_404(Schedule, pk=pk)
        data = {
                'date': schedule.date,
                'study_group': schedule.study_group,
        }
        schedule.delete()
        messages.success(request, "Schedule deleted successfully.")
        return self.handle_redirect(data)


class FillScheduleView(ScheduleBaseView):
    """
    View to populate the Schedule based on the selected study group, date,
    and applicable ScheduleTemplate entries for a given term.

    This view processes a form submission to fill the schedule for a study
    group within a specified week. It performs various validations, including
    checking for existing schedules, ensuring active terms are present, and
    verifying applicable templates before creating new Schedule entries.
    """
    permission_required = 'dictionaries.add_schedule'

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to fill the schedule based on selected study group
        and date.

        Parameters:
        - request: The HTTP request object containing POST data.

        Returns:
        - Redirects to a specified view with messages for success or failure.
        """
        study_group_request = request.POST.get("study_group", '')
        date_request = request.POST.get("date", '')
        data = {'date': date_request, 'study_group': study_group_request}

        if study_group_request and date_request:
            date_template = self.parse_date(date_request)
            start_of_week, end_of_week = self.get_week_range(date_template)

            # Check if Schedule entries already exist
            if self.schedule_exists(
                study_group_request, start_of_week, end_of_week
            ):
                messages.error(
                    request,
                    'Schedule entries already exist for the specified study '
                    'group and date range.'
                    )
                return self.handle_redirect(data)

            terms = self.get_terms(start_of_week, end_of_week)
            if not terms.exists():
                messages.error(
                    request,
                    'No active terms found for the specified date range.'
                    )
                return self.handle_redirect(data)

            combinations = self.create_combinations(start_of_week, terms)
            query = self.build_query(study_group_request, combinations)
            templates = ScheduleTemplate.objects.filter(query)
            if not templates.exists():
                messages.error(
                    request,
                    'No template found for the selected study group and terms.'
                    )
                return self.handle_redirect(data)

            self.fill_schedule(templates, start_of_week)
            messages.success(
                request,
                'Schedule filled successfully from template.'
                )
        else:
            messages.error(request, 'Study group and date are not specified.')

        return self.handle_redirect(data)

    def get_week_range(self, date_template):
        """
        Calculates the start and end dates of the week for the given date.

        Parameters:
        - date_template: A datetime object representing the reference date.

        Returns:
        - Tuple containing start and end dates of the week.
        """
        start_of_week = date_template - timedelta(days=date_template.weekday())
        end_of_week = (
            date_template + timedelta(days=(6 - date_template.weekday()))
        )
        return start_of_week, end_of_week

    def schedule_exists(self, study_group_request, start_of_week, end_of_week):
        """
        Checks if Schedule entries already exist for the specified study group
        within the given date range.

        Parameters:
        - study_group_request: Study group identifier from the request.
        - start_of_week: The start date of the week.
        - end_of_week: The end date of the week.

        Returns:
        - Boolean indicating whether Schedule entries exist in the specified
        range.
        """
        return Schedule.objects.filter(
            study_group=study_group_request,
            date__range=(start_of_week, end_of_week)
        ).exists()

    def get_terms(self, start_of_week, end_of_week):
        """
        Retrieves active terms that overlap with the specified week range.

        Parameters:
        - start_of_week: The start date of the week.
        - end_of_week: The end date of the week.

        Returns:
        - A QuerySet of Term instances that are active within the date range.
        """
        return Term.objects.filter(
            Q(date_from__lte=end_of_week) & Q(date_to__gte=start_of_week)
        ).order_by('date_from')

    def create_combinations(self, start_of_week, terms):
        """
        Creates a list of combinations of weekdays and active terms within the
        week.

        Parameters:
        - start_of_week: The start date of the week.
        - terms: A QuerySet of active Term instances.

        Returns:
        - A list of dictionaries, each containing a `weekday` and `term` for
        the dates in the specified week.
        """
        combinations = []
        for date_week in (start_of_week + timedelta(days=i) for i in range(7)):
            term = terms.filter(
                date_from__lte=date_week, date_to__gte=date_week
                ).first()
            if term:
                combinations.append(
                    {'weekday': date_week.weekday(), 'term': term}
                    )
        return combinations

    def build_query(self, study_group_request, combinations):
        """
        Constructs a query for filtering ScheduleTemplate instances based on
        study group and combinations of weekday and term.

        Parameters:
        - study_group_request: The study group identifier.
        - combinations: List of dictionaries with weekday-term pairs.

        Returns:
        - A Q object representing the query for matching ScheduleTemplates.
        """
        query = Q(
            study_group=study_group_request,
            weekday=combinations[0]['weekday'],
            term=combinations[0]['term'])
        for combo in combinations[1:]:
            query |= Q(
                study_group=study_group_request,
                weekday=combo['weekday'],
                term=combo['term'])
        return query

    def fill_schedule(self, templates, start_of_week):
        """
        Populates the Schedule by creating entries based on ScheduleTemplate
        instances.

        Parameters:
        - templates: QuerySet of ScheduleTemplate instances that match the
        filter criteria.
        - start_of_week: The start date of the week being populated.
        """
        for template in templates:
            Schedule.objects.create(
                date=start_of_week + timedelta(days=template.weekday),
                study_group=template.study_group,
                subject=template.subject,
                order_number=template.order_number
            )
