from django.test import TestCase
from .models import StudyGroup, Term
from django.core.exceptions import ValidationError
from datetime import date


class StudyGroupModel(TestCase):
    """
    Test cases for the StudyGroup model.
    """

    def setUp(self):
        # Create a StudyGroup instance
        self.study_group = StudyGroup.objects.create(name="101", active=True)

    def test_str_representation(self):
        """Test the string representation of StudyGroup."""
        self.assertEqual(str(self.study_group), "101")
    
    def test_study_group_name_cannot_be_empty(self):
        """
        Test if a StudyGroup cannot be created with an empty name.
        """
        study_group = StudyGroup(name='', active=True)
        with self.assertRaises(ValidationError):
            study_group.full_clean()  # This will trigger validation

    def test_unique_name(self):
        """Test that creating a StudyGroup with a duplicate name raises an IntegrityError."""
        StudyGroup.objects.create(name="102", active=True)
        with self.assertRaises(Exception):
            StudyGroup.objects.create(name="102", active=False)

    def test_active_default(self):
        """Test that the active field defaults to True."""
        new_group = StudyGroup.objects.create(name="103")
        self.assertTrue(new_group.active)


class TermModelTest(TestCase):
    """
    Test cases for the Term model.
    """

    def setUp(self):
        # Create a Term instance
        self.term = Term.objects.create(
            name="2024-2025 Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )

    def test_str_representation(self):
        """Test the string representation of Term."""
        self.assertEqual(
            str(self.term),
            "2024-2025 Term 1 - (2024-01-01-2024-05-31)"
        )

    def test_term_name_cannot_be_empty(self):
        """
        Test if a Term cannot be created with an empty name.
        """
        term = Term(
            name='',
            date_from='2024-01-01',
            date_to='2024-12-31',
            active=True
        )
        with self.assertRaises(ValidationError):
            term.full_clean()  # This will trigger validation

    def test_date_ordering(self):
        """Test that date_from is less than date_to."""
        term_invalid = Term(
            name="Invalid Term",
            date_from=date(2024, 5, 31),
            date_to=date(2024, 1, 1),
            active=True
        )
        with self.assertRaises(ValidationError):
            # This will invoke the clean method and validate
            term_invalid.clean()

    def test_overlapping_terms(self):
        """Test that overlapping terms raise a ValidationError."""
        # Create an overlapping term
        Term.objects.create(
            name="2024-2025 Term 2",
            date_from=date(2024, 4, 1),
            date_to=date(2024, 6, 30),
            active=True
        )

        term_overlapping = Term(
            name="2024-2025 Term 3",
            date_from=date(2024, 4, 15),
            date_to=date(2024, 5, 15),
            active=True
        )

        with self.assertRaises(ValidationError):
            # This will invoke the clean method and validate
            term_overlapping.clean()
