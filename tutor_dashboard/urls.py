from django.urls import path
from .views import dashboard, tutor_schedule_templates, tutor_schedules

app_name = 'tutor'
urlpatterns = [
    path('schedule-templates/', tutor_schedule_templates, name='schedule_templates'),
    path('schedules/', tutor_schedules, name='schedules'), 
]