from django.urls import path
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='tutor_dashboard'), 
]