from django.urls import path
from .views import ScheduleTemplateView, tutor_schedules
from .views import EditScheduleTemplateView

app_name = 'tutor'
urlpatterns = [
    path('schedule-templates/',
        ScheduleTemplateView.as_view(),
        name='schedule_templates'
    ),
    path(
        'schedule-templates/edit/<int:pk>/',
        EditScheduleTemplateView.as_view(),
        name='edit_schedule_template'
    ),
    path('schedules/', tutor_schedules, name='schedules'), 
]