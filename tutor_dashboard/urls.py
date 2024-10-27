from django.urls import path
from .views import ScheduleTemplateView, tutor_schedules

app_name = 'tutor'
urlpatterns = [
    path('schedule-templates/',
         ScheduleTemplateView.as_view(),
         name='schedule_templates'
    ),
    path('schedules/', tutor_schedules, name='schedules'), 
]