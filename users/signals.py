from django.contrib.auth.models import Group

GROUPS = ['Tutor', 'Student']

def create_groups(sender, **kwargs):
    for group_name in GROUPS:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f'Group "{group_name}" created.')
        else:
            print(f'Group "{group_name}" already exists.')
