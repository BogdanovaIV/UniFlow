from django.test import RequestFactory, TestCase
from django.db.models.query import QuerySet
from django.contrib.auth.models import User, Group
from dictionaries.models import StudyGroup
from users.models import UserProfile
from users.context_processors import user_profile_parameters


class ContextProcessorsTests(TestCase):
    """ Tests custom context processors for user groups. """
    def setUp(self):
        """
        Creates a student user and assigns them to the 'Student' group.
        Initializes a request factory for test requests.
        """
        self.student_user = User.objects.create_user(
            username='student@email.com',
            email='student@email.com',
            password='Password123!',
            first_name='student',
            last_name='student'
        )
        self.student_group = Group.objects.get(name='Student')
        self.student_user.groups.add(self.student_group)
        self.student_user.save()
        self.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        UserProfile.objects.create(
            user=self.student_user,
            study_group=self.study_group,
            checked=True
        )

        self.factory = RequestFactory()

    def test_user_groups_processor(self):
        """
        Tests that the user_groups context processor includes the user's groups
        in the context.
        """
        request = self.factory.get('/')
        request.user = self.student_user
        context = user_profile_parameters(request)

        self.assertIn('is_student', context)
        self.assertTrue(context['is_student'])

        self.assertIn('is_tutor', context)
        self.assertFalse(context['is_tutor'])

        self.assertIn('user_study_group', context)
        self.assertEqual(context['user_study_group'], self.study_group)

        self.assertIn('user_checked', context)
        self.assertTrue(context['user_checked'])
