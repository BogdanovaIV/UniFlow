from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from datetime import timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from dictionaries.forms import ScheduleFilterForm, ScheduleForm
from dictionaries.models import Schedule, WeekdayChoices


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
            'date': get_first_value('term'),
            'study_group': get_first_value('study_group'),
            'order_number': get_first_value('order_number'),
            'subject': get_first_value('subject'),
        }

    def handle_redirect(self, form):
        """
        Handle redirection after saving the form.
        """
        date = form.get('date')
        study_group = form.get('study_group').id
        return redirect(
            f"{reverse('tutor:schedule')}?date={date}"
            f"&study_group={study_group}"
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


class EditScheduleView(ScheduleBaseView):
    """
    View to edit a Schedule.
    """
    permission_required = 'dictionaries.change_schedule'
    
    def get(self, request, pk):
        """Render the form with the existing Schedule instance."""
        schedule = Schedule.objects.get(pk=pk)
        form = ScheduleForm(instance=schedule)
        return render(request, self.template_name, {'form': form})

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
            return self.handle_redirect(data)

        return render(request, self.template_name, {'form': form})

