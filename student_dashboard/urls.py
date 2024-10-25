from django.urls import path
from .views import dashboard

app_name ="student"
urlpatterns = [
    path('', dashboard, name='dashboard'), 
]