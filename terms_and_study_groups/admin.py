from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import StudyGroup, Term

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):

    # Display the name and active status
    list_display = ('name', 'active')
    # Add a filter for the active field
    list_filter = ('active',)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):

    # Display the name, date_from, date_to, and active status
    list_display = ('name', 'date_from', 'date_to', 'active')
    # Add a serach for the date_from and date_to fields 
    search_fields = ['date_from', 'date_to']
    # Add a filter for the active field
    list_filter = ('active',)
