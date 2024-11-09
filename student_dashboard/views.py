
from tutor_dashboard.views import ScheduleView

# Create your views here.
class StudentScheduleView(ScheduleView):
    """
    View for displaying and filtering the schedule based on user-selected date.

    This view provides functionality for displaying a filtered schedule based
    on the selected date and study group of the student, organizing schedule
    data by weekdays, and handling both GET and POST requests for schedule
    filtering.
    """
    template_name = 'student_dashboard/student-dashboard.html'
    url_name = 'student:dashboard'