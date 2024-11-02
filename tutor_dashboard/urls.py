from django.urls import path
from .views import (
    ScheduleTemplateView,
    AddScheduleTemplateView,
    EditScheduleTemplateView,
    DeleteScheduleTemplateView,
    ScheduleView,
    EditScheduleView,
    AddScheduleView,
    DeleteScheduleView
    )
app_name = 'tutor'
urlpatterns = [
    path(
        'schedule-templates/',
        ScheduleTemplateView.as_view(),
        name='schedule_templates'
    ),
    path(
        'schedule-templates/add/',
        AddScheduleTemplateView.as_view(),
        name='add_schedule_template'
    ),
    path(
        'schedule-templates/edit/<int:pk>/',
        EditScheduleTemplateView.as_view(),
        name='edit_schedule_template'
    ),
    path(
        'schedule-templates/delete/<int:pk>/',
        DeleteScheduleTemplateView.as_view(),
        name='delete_schedule_template'
    ),
    path(
        'schedule/',
        ScheduleView.as_view(),
        name='schedule'
    ),
    path(
        'schedule/add/',
        AddScheduleView.as_view(),
        name='add_schedule'
    ),
    path(
        'schedule/edit/<int:pk>/',
        EditScheduleView.as_view(),
        name='edit_schedule'
    ),
    path(
        'schedule/delete/<int:pk>/',
        DeleteScheduleView.as_view(),
        name='delete_schedule'
    ),
]