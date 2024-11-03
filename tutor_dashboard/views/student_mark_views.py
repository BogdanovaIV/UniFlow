from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from dictionaries.forms import StudentMarkForm
from dictionaries.models import Schedule, StudentMark


class EditStudentMarkView(View):
    """View to edit a StudentMark entry."""
    
    def post(self, request, schedule_pk, mark_pk):
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
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")
        
        return redirect(reverse('tutor:edit_schedule', args=[schedule_pk]))


class AddStudentMarkView(View):
    """View to add a StudentMark entry."""

    def post(self, request, schedule_pk):
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
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

        return redirect(reverse('tutor:edit_schedule', args=[schedule_pk]))