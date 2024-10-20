from django.test import TestCase
from django.contrib.auth.models import Group
from django.core.management import call_command

class SignalTestCase(TestCase):
    """
    Test cases for Signals.
    """
    def test_create_groups_signal(self):
        """Test that the required groups are created after migrations."""
        # Check that the groups were created
        self.assertEqual(Group.objects.count(), 2)  # Expecting 2 groups

        # Check that the correct groups were created
        group_names = [group.name for group in Group.objects.all()]
        self.assertIn('Tutor', group_names)
        self.assertIn('Student', group_names)