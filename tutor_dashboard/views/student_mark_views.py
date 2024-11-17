from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View

from dictionaries.forms import StudentMarkForm
from dictionaries.models import Schedule, StudentMark


class EditStudentMarkView(PermissionRequiredMixin, View):
    """
    View to edit an existing StudentMark entry.

    Ensures the user has permission to change student marks, checks for
    duplicate entries, validates the form, and provides feedback messages
    based on success or failure.
    """
    permission_required = 'dictionaries.change_studentmark'

    def post(self, request, schedule_pk, mark_pk):
        """
        Handles POST requests to update a StudentMark entry.

        Retrieves the StudentMark instance, validates the form data,
        checks for duplicates, and saves updates if valid.

        Parameters:
        - request: The HTTP request object containing POST data.
        - schedule_pk: Primary key of the schedule associated with the
        StudentMark.
        - mark_pk: Primary key of the StudentMark entry to be edited.

        Returns:
        - Redirects to the edit schedule page with appropriate messages.
        """
        student_mark = get_object_or_404(StudentMark, pk=mark_pk)
        form = StudentMarkForm(request.POST, instance=student_mark)
        if form.is_valid():
            student = form.cleaned_data['student']
            mark = form.cleaned_data['mark']
            # Check for duplicates
            duplicate_exists = StudentMark.objects.filter(
                Q(schedule=schedule_pk) & Q(student=student)
            ).exclude(pk=mark_pk).exists()

            if duplicate_exists:
                # Display duplicate error message
                messages.error(
                    request,
                    f"Mark for {student.get_full_name()} already exists for "
                    f"this schedule.")
            else:
                # Save and display success message
                form.save()
                messages.success(request, "Student mark updated successfully.")

            return redirect(
                reverse('tutor:edit_schedule',
                        args=[student_mark.schedule.pk])
            )

        # Form validation error message
        for field, errors in form.errors.items():
            messages.error(request, f"Error in {field}: {', '.join(errors)}")

        return redirect(reverse('tutor:edit_schedule', args=[schedule_pk]))


class AddStudentMarkView(PermissionRequiredMixin, View):
    """
    View to add a new StudentMark entry.

    This view checks for the required permission, validates the form input,
    verifies if a duplicate mark exists, and provides feedback messages
    based on the outcome.
    """
    permission_required = 'dictionaries.add_studentmark'

    def post(self, request, schedule_pk):
        """
        Handles POST requests to create a new StudentMark entry.

        Parameters:
        - request: The HTTP request object containing POST data.
        - schedule_pk: Primary key of the schedule to which the mark will be
        added.

        Returns:
        - Redirects to the edit schedule page with appropriate messages.
        """
        schedule = get_object_or_404(Schedule, pk=schedule_pk)
        form = StudentMarkForm(request.POST)

        if form.is_valid():
            student = form.cleaned_data['student']
            mark = form.cleaned_data['mark']

            # Check if a mark for this student and schedule already exists
            duplicate_exists = StudentMark.objects.filter(
                schedule=schedule, student=student
            ).exists()

            if duplicate_exists:
                # Display duplicate error message
                messages.error(
                    request,
                    f"A mark for {student.get_full_name()} already exists for "
                    f"this schedule."
                )
            else:
                # Save the new mark and display success message
                new_mark = form.save(commit=False)
                new_mark.schedule = schedule
                new_mark.save()
                messages.success(request, "Student mark added successfully.")

        # Form validation error message
        for field, errors in form.errors.items():
            messages.error(request, f"Error in {field}: {', '.join(errors)}")

        return redirect(reverse('tutor:edit_schedule', args=[schedule_pk]))


class DeleteStudentMarkView(PermissionRequiredMixin, View):
    """
    View to delete a StudentMark entry.

    This view ensures that the user has the required permission to delete
    a StudentMark, retrieves the specified entry, deletes it, and provides
    feedback to the user upon successful deletion.
    """
    permission_required = 'dictionaries.delete_studentmark'

    def post(self, request, schedule_pk, mark_pk):
        """
        Handles POST requests to delete a specific StudentMark entry.

        Parameters:
        - request: The HTTP request object.
        - schedule_pk: Primary key of the schedule associated with the mark.
        - mark_pk: Primary key of the StudentMark to delete.

        Returns:
        - Redirects to the edit schedule page with a success message.
        """
        student_mark = get_object_or_404(StudentMark, pk=mark_pk)
        student_mark.delete()
        messages.success(request, "Student mark deleted successfully.")
        return redirect(reverse('tutor:edit_schedule', args=[schedule_pk]))
