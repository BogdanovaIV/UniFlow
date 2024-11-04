from django.views.generic import View
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from datetime import timedelta, datetime
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import UserProfile
from dictionaries.forms import (
    ScheduleFilterForm,
    ScheduleForm
)
from dictionaries.models import (
    Schedule,
    WeekdayChoices,
    ScheduleTemplate,
    StudyGroup,
    Term,
    StudentMark
)


class ScheduleBaseView(PermissionRequiredMixin, View):
    """
    Base view for handling Schedule forms and display logic.
    """
    template_name = 'tutor_dashboard/edit_schedule.html'

    def get_initial_data(self, request):
        """
        Extract initial data from the request for the form.
        """
        def get_first_value(key):
            """Retrieve the first value for a given key from the request."""
            values = request.getlist(key)
            return values[0] if values else request.get(key)

        return {
            'date':
                datetime.strptime(get_first_value('date'), "%Y-%m-%d").date()
                if isinstance(get_first_value('date'), str)
                else get_first_value('date'),
            'study_group': get_first_value('study_group'),
            'order_number': get_first_value('order_number'),
            'subject': get_first_value('subject'),
        }

    def handle_redirect(self, form):
        """
        Handle redirection after saving the form.
        """
        date = form.get('date')
        study_group = (
            form.get('study_group').id 
            if isinstance(form.get('study_group'), StudyGroup) 
            else form.get('study_group')
        )
        return redirect(
            f"{reverse('tutor:schedule')}?date={date}"
            f"&study_group={study_group}",
        )


class ScheduleView(PermissionRequiredMixin, View):
    """
    View for displaying and filtering schedule based on user-selected
    term and study group.
    """
    template_name = 'tutor_dashboard/schedule.html'
    permission_required = 'dictionaries.view_schedule'

    def get(self, request):
        """
        Handles GET requests to display the schedule filter form.
        """
        
        date = request.GET.get('date') if 'date' in request.GET else ''
        study_group_id = (
            request.GET.get('study_group') if 'study_group' in request.GET
            else ''
        )
        form = ScheduleFilterForm(request.GET)
        
        if not form.is_valid():
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

        filter_params = form.get_filter_params()
        schedule, table_empty = self.get_schedule(
            filter_params
        )
        if table_empty:
            # Display message if no schedule is available for the selected
            # filters
            messages.info(
                request,
                "No schedule available for the selected date and study group."
            )
        else:
            # Display success message when schedule is successfully filtered
            messages.success(request, "Schedule displayed successfully.")

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'schedule': schedule,
                'table_empty': table_empty
            }
        )

    def post(self, request):
        """Handles POST requests to process the filter form submission."""
        form = ScheduleFilterForm(request.POST)
        date = request.POST.get('date') if 'date' in request.POST else ''
        study_group = (
            request.POST.get('study_group') if 'study_group' in request.POST
            else ''
        )

        return redirect(
            f"{reverse('tutor:schedule')}?date={date}"
            f"&study_group={study_group}"
        )

    def get_schedule(self, filter_params):
        """
        Retrieve and organize schedule based on term and group.
        """
        if filter_params['date__range'][0] and filter_params['study_group']:
            objects = Schedule.objects.filter(**filter_params)
            table_empty = not objects.exists()
        else:
            objects = Schedule.objects.none()
            table_empty = True

        return (
            self.get_full_week_schedule(objects, filter_params),
            table_empty
        )

    def get_full_week_schedule(self, objects, filter_params):
        """Organizes schedule by dates."""
        schedule = {
        value: {
            'label_weekday': label,
            'date': filter_params['date__range'][0] + timedelta(days=(value))
            if filter_params['date__range'][0] else '',
            'date_str': str(
                filter_params['date__range'][0] + timedelta(days=(value))
                ) if filter_params['date__range'][0] else '',
            'details': {order: {'id': '','subject': '', 'homework': ''}
                        for order in range(1, 11)}
        }
        for value, label in WeekdayChoices.choices
        }
        for object in objects:
            schedule[object.date.weekday()]['details'][object.order_number] = {
                'id': object.id,
                'subject': object.subject,
                'homework': object.homework
            }
        return schedule


class EditScheduleView(ScheduleBaseView):
    """
    View to edit a Schedule.
    """
    permission_required = 'dictionaries.change_schedule'
    
    def get(self, request, pk):
        """Render the form with the existing Schedule instance."""
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
        Save the updated Schedule and redirect or reload the form
        on error.
        """
        schedule = Schedule.objects.get(pk=pk)
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            data = {
                'date':form.cleaned_data.get('date'),
                'study_group':form.cleaned_data.get('study_group'),
            }
            messages.success(request, "Schedule updated successfully.")
            return self.handle_redirect(data)

        # Form validation error message
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

        return render(request, self.template_name, {'form': form})


class AddScheduleView(ScheduleBaseView):
    """
    View to add a new Schedule. Uses initial data from query parameters.
    """
    permission_required = 'dictionaries.add_schedule'
    
    def get(self, request):
        """Render the form to add a new Schedule."""
        initial_data = self.get_initial_data(request.GET)
        form = ScheduleForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Process the form submission to add a new Schedule."""

        initial_data = self.get_initial_data(request.POST)
        form = ScheduleForm(request.POST, initial=initial_data)

        if form.is_valid():
            form.save()
            data = {
                'date':form.cleaned_data.get('date'),
                'study_group':form.cleaned_data.get('study_group'),
            }
            messages.success(request, "Schedule added successfully.")
            return self.handle_redirect(data)
        
        # Form validation error message
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

        return render(request, self.template_name, {'form': form})


class DeleteScheduleView(ScheduleBaseView):
    """
    View to delete a Schedule.
    """
    permission_required = 'dictionaries.delete_schedule'
    
    def post(self, request, pk):
        """
        Handles the POST request to delete the specified Schedule 
        and redirects to the schedule list.
        """
        schedule = get_object_or_404(Schedule, pk=pk)
        data = {
                'date':schedule.date,
                'study_group':schedule.study_group,
        }
        schedule.delete()
        messages.success(request, "Schedule deleted successfully.")
        return self.handle_redirect(data)


class FillScheduleView(ScheduleBaseView):
    """
    View to fill the Schedule based on selected study group and date.
    Checks for existing schedules and uses applicable terms for filling.
    """
    permission_required = 'dictionaries.add_schedule'

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to fill the schedule. Validates 
        study group and date, checks for existing entries, 
        and fills the schedule based on templates.
        """
        study_group_request = request.POST.get("study_group", '')
        date_request = request.POST.get("date", '')
        data = {'date': date_request, 'study_group': study_group_request}

        if study_group_request and date_request:
            date_template = self.parse_date(date_request)
            start_of_week, end_of_week = self.get_week_range(date_template)

            # Check if Schedule entries already exist
            if self.schedule_exists(
                study_group_request, start_of_week, end_of_week):
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

    def get_study_group(self, request):
        """ Retrieves the study group from the request. """
        return request.POST.get("study_group", '')

    def parse_date(self, date_request):
        """Parses the date string to a date object."""
        if isinstance(date_request, str):
            # Convert the date string to a date object
            parsed_date = datetime.strptime(date_request, "%Y-%m-%d").date()
        else:
            parsed_date = date_request

        return parsed_date

    def get_week_range(self, date_template):
        """ Returns the start and end of the week for a given date. """
        start_of_week = date_template - timedelta(days=date_template.weekday())
        end_of_week = (
            date_template + timedelta(days=(6 - date_template.weekday()))
        )
        return start_of_week, end_of_week

    def schedule_exists(self, study_group_request, start_of_week, end_of_week):
        """ Checks for existing Schedule entries within the specified range. """
        return Schedule.objects.filter(
            study_group=study_group_request,
            date__range=(start_of_week, end_of_week)
        ).exists()

    def get_terms(self, start_of_week, end_of_week):
        """ Retrieves active terms overlapping with the specified week. """
        return Term.objects.filter(
            Q(date_from__lte=end_of_week) & Q(date_to__gte=start_of_week)
        ).order_by('date_from')

    def create_combinations(self, start_of_week, terms):
        """ Creates a list of weekday-term combinations for the week. """
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
        Builds a query for filtering ScheduleTemplate based on combinations.
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
        """ Fills the Schedule by creating entries based on the templates. """
        for template in templates:
            Schedule.objects.create(
                date=start_of_week + timedelta(days=template.weekday),
                study_group=template.study_group,
                subject=template.subject,
                order_number=template.order_number
            )
