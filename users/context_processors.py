from django.contrib.auth.models import Group
from users.models import UserProfile

def user_profile_parameters(request):
    user_study_group = []
    user_checked = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(
            user=request.user
        )
        if user_profile.exists():
            first_profile = user_profile.first()
            user_study_group = first_profile.study_group
            user_checked = first_profile.checked 
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        user_groups = request.user.groups.all()
        
    return {
        'is_tutor': (tutor_group in user_groups)
        if request.user.is_authenticated else False,
        'is_student': (student_group in user_groups)
        if request.user.is_authenticated else False,
        'user_study_group': user_study_group,
        'user_checked': user_checked
    }