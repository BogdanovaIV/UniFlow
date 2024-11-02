from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from datetime import timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from dictionaries.forms import ScheduleFilterForm
from dictionaries.models import Schedule, WeekdayChoices


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

        filter_params = form.get_filter_params()
        schedule, table_empty = self.get_schedule(
            filter_params
        )

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
            table_empty = False
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
