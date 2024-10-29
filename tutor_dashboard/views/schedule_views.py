from django.views.generic import View
from django.shortcuts import render

def tutor_schedules(request):
    """
    Renders the Schedule page
    """
    return render(
        request,
        "tutor_dashboard/schedule.html",
    )
