from django.urls import path
from .views import StudentScheduleView

app_name ="student"
urlpatterns = [
    path('', StudentScheduleView.as_view(), name='dashboard'), 
]