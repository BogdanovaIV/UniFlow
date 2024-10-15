from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import StudyGroup

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):

    # Display the name and active status
    list_display = ('name', 'active')
    # Add a filter for the active field
    list_filter = ('active',)
