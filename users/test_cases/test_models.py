from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dictionaries.models import StudyGroup
from users.models import UserProfile


class TestUserProfileModel(TestCase):
    """ Test cases for the UserProfile model. """
    def setUp(self):
        """ Create a user and study group for testing. """
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.study_group = StudyGroup.objects.create(name='Test Group')

    def test_user_profile_creation(self):
        """ Test creating a UserProfile with a user. """
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        # study_group should be None by default
        self.assertIsNone(profile.study_group)
        # checked should default to False
        self.assertFalse(profile.checked)

    def test_user_profile_with_study_group(self):
        """ Test creating a UserProfile with a study group. """
        profile = UserProfile.objects.create(
            user=self.user,
            study_group=self.study_group
        )
        self.assertEqual(profile.study_group, self.study_group)

    def test_clean_method_with_checked_and_empty_study_group(self):
        """
        Test that a ValidationError is raised if checked is True but
        study_group is empty.
        """
        profile = UserProfile(user=self.user, checked=True)

        with self.assertRaises(ValidationError):
            # This should raise a ValidationError since study_group is None
            profile.clean()

    def test_clean_method_with_checked_and_filled_study_group(self):
        """
        Test that no ValidationError is raised if checked is True and
        study_group is filled.
        """
        profile = UserProfile(
            user=self.user,
            checked=True,
            study_group=self.study_group
        )
        try:
            # This should not raise a ValidationError
            profile.clean()
        except ValidationError:
            self.fail(
                "ValidationError was raised when it shouldn't have been."
            )

    def test_string_representation(self):
        """ Test the string representation of UserProfile. """
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), "testuser's Profile")
