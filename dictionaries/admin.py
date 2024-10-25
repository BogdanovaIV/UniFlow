from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import StudyGroup, Term, Subject, ScheduleTemplate


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    """
    Admin interface for managing StudyGroup instances.

    Attributes:
        list_display (tuple): Fields to display in the list view of StudyGroup
        instances.
        list_filter (tuple): Fields that can be used to filter the list view.
    """

    # Display the name and active status
    list_display = ('name', 'active')
    # Add a filter for the active field
    list_filter = ('active',)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Term instances.

    Attributes:
        list_display (tuple): Fields to display in the list view of Term
        instances.
        search_fields (list): Fields that can be searched in the list view.
        list_filter (tuple): Fields that can be used to filter the list view.
    """

    # Display the name, date_from, date_to, and active status
    list_display = ('name', 'date_from', 'date_to', 'active')
    # Add a serach for the date_from and date_to fields 
    search_fields = ['date_from', 'date_to']
    # Add a filter for the active field
    list_filter = ('active',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Subject instances.

    Attributes:
        list_display (tuple): Fields to display in the list view of Subject
        instances.
        list_filter (tuple): Fields that can be used to filter the list view.
    """

    # Display the name and active status
    list_display = ('name', 'active')
    # Add a filter for the active field
    list_filter = ('active',)


@admin.register(ScheduleTemplate)
class ScheduleTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ScheduleTemplate instances.

    Attributes:
        list_display (tuple): Fields to display in the list view of 
        ScheduleTemplate instances.
        list_filter (tuple): Fields that can be used to filter the list view.
    """
    
    # Display the term, study_group, weekday, order_number and subject
    list_display = (
        'term',
        'study_group',
        'weekday',
        'order_number',
        'subject'
    )

    # Add a filter for the weekday field
    list_filter = ('weekday','term', 'study_group')
