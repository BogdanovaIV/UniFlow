from django.contrib.auth.models import Group

def user_groups(request):
    return {
        'user_groups': request.user.groups.all()
        if request.user.is_authenticated else [],
    }