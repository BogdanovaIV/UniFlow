from django.views.generic import View
from django.shortcuts import render
from dictionaries.models import ScheduleTemplate, WeekdayChoices
from dictionaries.forms import ScheduleTemplateFilterForm

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
        form = ScheduleTemplateFilterForm()
        schedule_templates = self.get_full_week_schedule({})
        return render(
            request,
            self.template_name,
            {'form': form, 'schedule_templates': schedule_templates}
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
        form = ScheduleTemplateFilterForm(request.POST)
        schedule_templates = ScheduleTemplate.objects.none()
        if form.is_valid():
            term = form.cleaned_data['term']
            study_group = form.cleaned_data['study_group']
            
            templates = ScheduleTemplate.objects.filter(
                term=term, 
                study_group=study_group
            )

            # Group schedule templates by weekday and order number
            schedule_templates = self.get_full_week_schedule(templates)
            
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'schedule_templates': schedule_templates}
        )

    def get_full_week_schedule(self, templates):
        """
        Organizes schedule templates by weekday, ensuring all order numbers
        (1–10) are present for each weekday.
        """
        # Initialize schedule_templates with all weekdays and order numbers
        # (1–10)
        schedule = {
            value: [label, {order: '' for order in range(1, 11)}]
            for (value, label) in WeekdayChoices.choices
        }
        # Populate the schedule with actual templates from the queryset
        for template in templates:
            schedule[template.weekday][1][template.order_number] = template.subject

        return schedule

def tutor_schedules(request):
    """
    Renders the Schedule page
    """
    return render(
        request,
        "tutor_dashboard/schedule.html",
    )

def tutor_schedule_templates(request):
    """
    Renders the Schedule templates page
    """
    return render(
        request,
        "tutor_dashboard/schedule-templates.html",
    )