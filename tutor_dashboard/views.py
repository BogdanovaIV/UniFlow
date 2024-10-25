from django.shortcuts import render

# Create your views here.
def dashboard(request):
    """
    Renders the Dashboard page
    """
    return render(
        request,
        "tutor_dashboard/tutor-dashboard.html",
    )

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