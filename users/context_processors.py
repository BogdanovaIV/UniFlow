from django.contrib.auth.models import Group
from users.models import UserProfile


def user_profile_parameters(request):
    """
    Context processor to provide user-specific profile data to the template.

    Args:
        request (HttpRequest): The HTTP request object containing the user
        details.

    Returns:
        dict: A dictionary containing the following user-specific context:
            - 'is_tutor': Boolean indicating if the user belongs to the "Tutor"
            group.
            - 'is_student': Boolean indicating if the user belongs to the
            "Student" group.
            - 'user_study_group': The user's study group, if available.
            - 'user_checked': Boolean indicating if the user's profile is
            verified (checked).
    """
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
