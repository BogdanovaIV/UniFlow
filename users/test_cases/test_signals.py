from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from users.signals import create_groups, GROUPS


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

    def test_create_groups_when_groups_exist(self):
        """Test that no duplicate groups are created if they already exist."""

        create_groups(sender=None)

        # Ensure no additional groups were created
        self.assertEqual(Group.objects.count(), 2)

        # Ensure existing groups still exist and are not duplicated
        self.assertTrue(Group.objects.filter(name='Tutor').exists())
        self.assertTrue(Group.objects.filter(name='Student').exists())

        # Verify permissions remain assigned
        for group_name, perms in GROUPS.items():
            group = Group.objects.get(name=group_name)
            for perm_codename in perms:
                permission = Permission.objects.get(codename=perm_codename)
                self.assertIn(
                    permission,
                    group.permissions.all(),
                    f"Permission '{perm_codename}' not assigned to group "
                    f"'{group_name}'."
                )
