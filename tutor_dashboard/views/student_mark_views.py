from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from dictionaries.forms import StudentMarkForm
from dictionaries.models import Schedule, StudentMark


class EditStudentMarkView(View):
    """View to edit a StudentMark entry."""
    
    def post(self, request, schedule_pk, mark_pk):
        student_mark = get_object_or_404(StudentMark, pk=mark_pk)
        form = StudentMarkForm(request.POST, instance=student_mark)
        if form.is_valid():
            form.save()
        return redirect(reverse('tutor:edit_schedule', args=[student_mark.schedule.pk]))
