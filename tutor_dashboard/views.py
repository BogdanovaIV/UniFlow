from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from dictionaries.models import ScheduleTemplate, WeekdayChoices
from dictionaries.forms import ScheduleTemplateFilterForm
from dictionaries.forms import ScheduleTemplateForm


class ScheduleTemplateBaseView(View):
    """
    Base view for handling ScheduleTemplate forms and display logic.
    """
    template_name = 'tutor_dashboard/edit_schedule_template.html'

    def get_initial_data(self, request):
        """
        Extract initial data from the request for the form.
        """
        return {
            'term': (
                request.POST.getlist('term')[0] if request.POST.getlist('term')
                else request.GET.get('term')
            ),
            'study_group': (
                request.POST.getlist('study_group')[0]
                if request.POST.getlist('study_group')
                else request.GET.get('study_group')
            ),
            'weekday': (
                request.POST.getlist('weekday')[0]
                if request.POST.getlist('weekday')
                else request.GET.get('weekday')
            ),
            'order_number': (
                request.POST.getlist('order_number')[0]
                if request.POST.getlist('order_number')
                else request.GET.get('order_number')
            ),
        }

    def handle_redirect(self, form):
        """
        Handle redirection after saving the form.
        """
        term = form.cleaned_data.get('term').id
        study_group = form.cleaned_data.get('study_group').id
        return redirect(
            f"{reverse('tutor:schedule_templates')}?term={term}"
            f"&study_group={study_group}"
        )


class ScheduleTemplateView(View):
    """
    View for displaying and filtering schedule templates based on user-selected
    term and study group.
    """
    template_name = 'tutor_dashboard/schedule-templates.html'

    def get(self, request):
        """
        Handles GET requests to display the schedule templates filter form.
        """
        
        term_id = request.GET.get('term') if 'term' in request.GET else ''
        study_group_id = (
            request.GET.get('study_group') if 'study_group' in request.GET
            else ''
        )

        form = ScheduleTemplateFilterForm(
            initial={'term': term_id, 'study_group': study_group_id}
        )

        schedule_templates, table_empty = self.get_schedule_templates(
            term_id,
            study_group_id
        )

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'schedule_templates': schedule_templates,
                'table_empty': table_empty
            }
        )

    def post(self, request):
        """Handles POST requests to process the filter form submission."""
        form = ScheduleTemplateFilterForm(request.POST)
        term = request.POST.get('term') if 'term' in request.POST else ''
        study_group = (
            request.POST.get('study_group') if 'study_group' in request.POST
            else ''
        )

        return redirect(
            f"{reverse('tutor:schedule_templates')}?term={term}"
            f"&study_group={study_group}"
        )

    def get_schedule_templates(self, term_id, study_group_id):
        """
        Retrieve and organize schedule templates based on term and group.
        """
        if term_id and study_group_id:
            templates = ScheduleTemplate.objects.filter(
                term=term_id,
                study_group=study_group_id
            )
            table_empty = False
        else:
            templates = ScheduleTemplate.objects.none()
            table_empty = True

        return self.get_full_week_schedule(templates), table_empty

    def get_full_week_schedule(self, templates):
        """Organizes schedule templates by weekday."""
        schedule = {
            value: [label, {
                order: {'subject': '', 'id': ''} for order in range(1, 11)
                }]
            for (value, label) in WeekdayChoices.choices
        }

        for template in templates:
            schedule[template.weekday][1][template.order_number] = {
                'subject': template.subject, 'id': template.id
            }

        return schedule

class EditScheduleTemplateView(ScheduleTemplateBaseView):
    """
    View to edit a ScheduleTemplate.
    """

    def get(self, request, pk):
        """Render the form with the existing ScheduleTemplate instance."""
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(instance=schedule_template)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        """
        Save the updated ScheduleTemplate and redirect or reload the form
        on error.
        """
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(request.POST, instance=schedule_template)

        if form.is_valid():
            form.save()
            return self.handle_redirect(form)

        return render(request, self.template_name, {'form': form})


class AddScheduleTemplateView(ScheduleTemplateBaseView):
    """
    View to add a new ScheduleTemplate. Uses initial data from query parameters.
    """

    def get(self, request):
        """Render the form to add a new ScheduleTemplate."""
        initial_data = self.get_initial_data(request)
        form = ScheduleTemplateForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Process the form submission to add a new ScheduleTemplate."""
        initial_data = self.get_initial_data(request)
        form = ScheduleTemplateForm(request.POST, initial=initial_data)

        if form.is_valid():
            form.save()
            return self.handle_redirect(form)

        return render(request, self.template_name, {'form': form})


def tutor_schedules(request):
    """
    Renders the Schedule page
    """
    return render(
        request,
        "tutor_dashboard/schedule.html",
    )
