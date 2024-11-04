from django.contrib.auth.models import Group, Permission
from dictionaries.models import StudyGroup


GROUPS = {
    'Tutor': [
        'view_studygroup',
        'view_term',
        'view_subject',
        'view_scheduletemplate',
        'add_scheduletemplate',
        'change_scheduletemplate',
        'delete_scheduletemplate',
        'view_schedule',
        'add_schedule',
        'change_schedule',
        'delete_schedule',
        'view_studentmark',
        'add_studentmark',
        'change_studentmark',
        'delete_studentmark',
        ],
    'Student': [
        'view_studygroup',
        'view_term',
        'view_subject',
        'view_schedule',
        'view_studentmark'
        ]
}

def create_groups(sender, **kwargs):
    for group_name, perms in GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f'Group "{group_name}" created.')
        else:
            print(f'Group "{group_name}" already exists.')

        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)