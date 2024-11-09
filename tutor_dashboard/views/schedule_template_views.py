from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from dictionaries.models import ScheduleTemplate, WeekdayChoices
from dictionaries.forms import ScheduleTemplateFilterForm, ScheduleTemplateForm


class ScheduleTemplateBaseView(PermissionRequiredMixin, View):
    """
    Base view for handling ScheduleTemplate forms and display logic.

    Attributes:
        template_name (str): The template used for rendering the form.
    """
    template_name = 'tutor_dashboard/edit_schedule_template.html'

    def get_initial_data(self, request):
        """
        Extract initial data from the request for pre-filling form fields.

        Parameters:
            request (HttpRequest): The HTTP request object containing GET
            parameters.

        Returns:
            dict: Initial form data, including term, study_group, weekday,
            and order_number fields, based on request parameters.
        """
        def get_first_value(key):
            """Retrieve the first value for a given key from the request."""
            values = request.getlist(key)
            return values[0] if values else request.get(key)

        return {
            'term': get_first_value('term'),
            'study_group': get_first_value('study_group'),
            'weekday': get_first_value('weekday'),
            'order_number': get_first_value('order_number'),
        }

    def handle_redirect(self, form):
        """
        Handle redirection after a form submission, applying filters for term
        and study group.

        Parameters:
            form (dict): The cleaned form data after successful validation.

        Returns:
            HttpResponseRedirect: A redirection to the schedule templates list
            page with term and study group filters as URL query parameters.
        """
        term = form.get('term').id
        study_group = form.get('study_group').id
        return redirect(
            f"{reverse('tutor:schedule_templates')}?term={term}"
            f"&study_group={study_group}"
        )


class ScheduleTemplateView(PermissionRequiredMixin, View):
    """
    View for displaying and filtering schedule templates based on user-selected
    term and study group.

    Attributes:
        template_name (str): The template used for rendering the schedule
        templates.
        permission_required (str): Permission required to view schedule
        templates.
    """
    template_name = 'tutor_dashboard/schedule-templates.html'
    permission_required = 'dictionaries.view_scheduletemplate'

    def get(self, request):
        """
        Handles GET requests to display the schedule templates filter form
        and the filtered schedule templates, if selected.

        Parameters:
            request (HttpRequest): The HTTP request object containing GET
            parameters.

        Returns:
            HttpResponse: Rendered template with the filter form, schedule
            templates, and messages indicating success or errors.
        """
        term_id = request.GET.get('term') if 'term' in request.GET else ''
        study_group_id = (
            request.GET.get('study_group') if 'study_group' in request.GET
            else ''
        )
        form = ScheduleTemplateFilterForm(request.GET)
        if request.GET and not form.is_valid():
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

        schedule_templates, table_empty = self.get_schedule_templates(
            term_id,
            study_group_id
        )

        if table_empty and request.GET:
            # Display message if no schedule template is available for the
            # selected filters
            messages.info(
                request,
                "No schedule template available for the selected date and "
                "study group."
            )
        elif request.GET:
            # Display success message when schedule template is successfully
            # filtered
            messages.success(
                request, "Schedule template displayed successfully."
            )

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'schedule_templates': schedule_templates,
                'table_empty': table_empty,
                'selection_valid': form.is_valid()
            }
        )

    def post(self, request):
        """
        Handles POST requests to process and redirect with filter form data.

        Parameters:
            request (HttpRequest): The HTTP request object containing POST
            parameters.

        Returns:
            HttpResponseRedirect: Redirects to the same view with term and
            study_group as URL query parameters.
        """
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
        Retrieve and organize schedule templates based on selected term and
        study group.

        Parameters:
            term_id (str): ID of the selected term.
            study_group_id (str): ID of the selected study group.

        Returns:
            tuple: A tuple containing:
            - dict: Organized schedule templates for the week.
            - bool: Indicates if the table is empty (no templates found).
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
        """
        Organizes schedule templates by weekday for display.

        Parameters:
            templates (QuerySet): ScheduleTemplate queryset filtered by term
            and study group.

        Returns:
            dict: A dictionary organizing schedule templates by weekday, with
            keys as weekday values and each containing a dictionary of subjects
            per order number.
        """
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

    Attributes:
        template_name (str): The template used for rendering the schedule
        templates.
        permission_required (str): Permission required to view schedule
        templates.
    """
    permission_required = 'dictionaries.change_scheduletemplate'

    def get(self, request, pk):
        """
        Render the form with the existing ScheduleTemplate instance.

        Parameters:
            request (HttpRequest): The HTTP request object.
            pk (int): Primary key of the ScheduleTemplate.

        Returns:
            HttpResponse: Rendered template with the form.
        """
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(instance=schedule_template)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        """
        Save the updated ScheduleTemplate and redirect or reload the form
        on error.

        Parameters:
            request (HttpRequest): The HTTP request object.
            pk (int): Primary key of the ScheduleTemplate.

        Returns:
            HttpResponse: Redirects on success or renders form on failure.
        """
        schedule_template = ScheduleTemplate.objects.get(pk=pk)
        form = ScheduleTemplateForm(request.POST, instance=schedule_template)

        if form.is_valid():
            form.save()
            data = {
                'term': form.cleaned_data.get('term'),
                'study_group': form.cleaned_data.get('study_group'),
            }
            messages.success(
                request,
                "Schedule template updated successfully."
            )
            return self.handle_redirect(data)

        # Form validation error message
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

        return render(request, self.template_name, {'form': form})


class AddScheduleTemplateView(ScheduleTemplateBaseView):
    """
    View to add a new ScheduleTemplate. Uses initial data from query
    parameters.

    Attributes:
        template_name (str): The template used for rendering the schedule
        templates.
        permission_required (str): Permission required to view schedule
        templates.
    """
    permission_required = 'dictionaries.add_scheduletemplate'

    def get(self, request):
        """
        Renders the form to add a new ScheduleTemplate.

        Parameters:
            request (HttpRequest): The HTTP request object containing GET
            parameters.

        Returns:
            HttpResponse: Rendered template with an empty form for adding a new
            ScheduleTemplate.
        """
        initial_data = self.get_initial_data(request.GET)
        form = ScheduleTemplateForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Processes form submission to add a new ScheduleTemplate instance.
        Validates form data and saves if valid; otherwise, reloads form with
        errors.

        Parameters:
            request (HttpRequest): The HTTP request object containing POST
            data.

        Returns:
            HttpResponse: Redirects on successful submission or re-renders form
            with errors.
        """

        initial_data = self.get_initial_data(request.POST)
        form = ScheduleTemplateForm(request.POST, initial=initial_data)

        if form.is_valid():
            form.save()
            data = {
                'term': form.cleaned_data.get('term'),
                'study_group': form.cleaned_data.get('study_group'),
            }
            messages.success(request, "Schedule template added successfully.")
            return self.handle_redirect(data)

        # Form validation error message
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

        return render(request, self.template_name, {'form': form})


class DeleteScheduleTemplateView(ScheduleTemplateBaseView):
    """
    View to delete a ScheduleTemplate.

    Attributes:
        permission_required (str): Permission required to delete schedule
        templates.
    """
    permission_required = 'dictionaries.delete_scheduletemplate'

    def post(self, request, pk):
        """
        Handles the POST request to delete the specified ScheduleTemplate
        and redirects to the schedule templates list.

        Parameters:
            request (HttpRequest): The HTTP request object containing POST
            data.
            pk (int): Primary key of the ScheduleTemplate to be deleted.

        Returns:
            HttpResponse: Redirects to the schedule templates list after
            successful deletion.
        """
        schedule_template = get_object_or_404(ScheduleTemplate, pk=pk)
        data = {
                'term': schedule_template.term,
                'study_group': schedule_template.study_group,
        }
        schedule_template.delete()
        messages.success(request, "Schedule template deleted successfully.")
        return self.handle_redirect(data)
