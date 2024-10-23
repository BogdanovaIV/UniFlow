from django.shortcuts import render

# Create your views here.
def dashboard(request):
    """
    Renders the Dashboard page
    """
    return render(
        request,
        "student_dashboard/student-dashboard.html",
    )
