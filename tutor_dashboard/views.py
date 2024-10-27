from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from dictionaries.models import ScheduleTemplate, WeekdayChoices
from dictionaries.forms import ScheduleTemplateFilterForm
from dictionaries.forms import ScheduleTemplateForm

class ScheduleTemplateView(View):
    """
    View for displaying and filtering schedule templates based on user-selected
    term and study group.

    Attributes:
        template_name (str): The name of the template to render for this view.
    """
    template_name = 'tutor_dashboard/schedule-templates.html'

    def get(self, request):
        """
        Handles GET requests to display the schedule templates filter form and
        the full week's schedule.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered template with an empty form and the full
            week's schedule.
        """
        term_id = request.GET.get('term')
        study_group_id = request.GET.get('study_group')

        form = ScheduleTemplateFilterForm(
            initial={'term': term_id, 'study_group': study_group_id}
        )
        table_empty = True
        schedule_templates = None
        if term_id and study_group_id:
            schedule_templates = self.get_full_week_schedule(
                ScheduleTemplate.objects.filter(
                    term=term_id, study_group=study_group_id
                )
            )
            table_empty = False
        else:
            schedule_templates = self.get_full_week_schedule({})

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
        """
        Handles POST requests to process the filter form submission and display
        filtered schedule templates.

        Args:
            request (HttpRequest): The HTTP request object containing form data.

        Returns:
            HttpResponse: Rendered template with the filter form and filtered
            schedule templates.
        """
        schedule_templates = ScheduleTemplate.objects.none()
        form = ScheduleTemplateFilterForm(request.POST)
        term = request.POST.get('term')
        study_group = request.POST.get('study_group')

        return redirect(
            f"{reverse(
                'tutor:schedule_templates'
                )}?term={term}&study_group={study_group}"
        )

    def get_full_week_schedule(self, templates):
        """
        Organizes schedule templates by weekday, ensuring all order numbers
        (1–10) are present for each weekday.
        """
        # Initialize schedule_templates with all weekdays and order numbers
        # (1–10)
        schedule = {
            value: [label, {
                order: {'subject':'', 'id':''} for order in range(1, 11)
                }] for (value, label) in WeekdayChoices.choices
        }

        # Populate the schedule with actual templates from the queryset
        for template in templates:
            schedule[template.weekday][1][template.order_number] = {
                'subject': template.subject, 'id':template.id
            }

        return schedule

class EditScheduleTemplateView(View):
    """
    View to edit a ScheduleTemplate. Renders a form with existing data for GET,
    saves changes for valid POST, and redirects to schedule list with term and
    group parameters.
    """
    template_name = 'tutor_dashboard/edit_schedule_template.html'

    def get(self, request, pk):
        """Render the form with the existing ScheduleTemplate instance."""
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(instance=schedule_template)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        """
        Save the updated ScheduleTemplate and redirect or reload the form on
        error.
        """
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(request.POST, instance=schedule_template)
        if form.is_valid():
            form.save()
            term = form.cleaned_data.get('term').id
            study_group = form.cleaned_data.get('study_group').id
            return redirect(
                f"{reverse(
                    'tutor:schedule_templates'
                    )}?term={term}&study_group={study_group}"
            )
        return render(request, self.template_name, {'form': form})

def tutor_schedules(request):
    """
    Renders the Schedule page
    """
    return render(
        request,
        "tutor_dashboard/schedule.html",
    )
