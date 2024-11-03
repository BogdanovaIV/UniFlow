from django.test import TestCase
from datetime import date, timedelta
from django.contrib.auth.models import User
from .forms import (
    ScheduleTemplateFilterForm,
    ScheduleTemplateForm,
    ScheduleFilterForm,
    ScheduleForm,
    StudentMarkForm)
from .models import (
    Term,
    StudyGroup,
    ScheduleTemplate,
    Subject,
    WeekdayChoices,
    Schedule
)

class ScheduleTemplateFilterFormTests(TestCase):
    """
    Test suite for ScheduleTemplateFilterForm to ensure form fields,
    querysets, and validation behave correctly.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data by creating active and inactive terms 
        and study groups for validating form filtering and field behavior.
        """
        cls.term1 = Term.objects.create(
            name="Term 1",
            date_from='2024-01-01',
            date_to='2024-05-31',
            active=True
        )
        cls.term2 = Term.objects.create(
            name="Term 2",
            date_from='2024-09-01',
            date_to='2024-12-25',
            active=False
        )
        cls.group1 = StudyGroup.objects.create(name="Group A", active=True)
        cls.group2 = StudyGroup.objects.create(name="Group B", active=False)

    def test_form_fields(self):
        """
        Validates that the form includes 'term' and 'study_group' fields 
        and confirms that their labels are correctly set.
        """
        form = ScheduleTemplateFilterForm()
        # Check if 'term' and 'study_group' fields are in the form
        self.assertIn('term', form.fields)
        self.assertIn('study_group', form.fields)
        # Verify labels for each field
        self.assertEqual(form.fields['term'].label, "Term")
        self.assertEqual(form.fields['study_group'].label, "Study Group")

    def test_queryset_for_term_field(self):
        """
        Checks that the 'term' field's queryset includes only active terms 
        by verifying that inactive terms are excluded.
        """
        form = ScheduleTemplateFilterForm()
        terms_queryset = form.fields['term'].queryset
        self.assertIn(self.term1, terms_queryset)
        self.assertNotIn(self.term2, terms_queryset)

    def test_queryset_for_study_group_field(self):
        """
        Confirms that the 'study_group' field's queryset includes only active 
        study groups and excludes inactive ones.
        """
        form = ScheduleTemplateFilterForm()
        study_groups_queryset = form.fields['study_group'].queryset
        self.assertIn(self.group1, study_groups_queryset)
        self.assertNotIn(self.group2, study_groups_queryset)

    def test_form_is_valid_with_correct_data(self):
        """
        Ensures that the form is valid when provided with data for both 
        'term' and 'study_group' fields.
        """
        form_data = {'term': self.term1.id, 'study_group': self.group1.id}
        form = ScheduleTemplateFilterForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_is_invalid_with_missing_data(self):
        """
        Tests that the form is invalid if required fields are missing, 
        such as when only the 'term' field is provided.
        """
        form_data = {'term': self.term1.id}
        form = ScheduleTemplateFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('study_group', form.errors)


class ScheduleTemplateFormTests(TestCase):
    """
    Test suite for ScheduleTemplateForm to ensure form fields,
    querysets, and validation behave correctly.
    """

    def setUp(self):
        """Create necessary objects for ScheduleTemplate."""
        self.term = Term.objects.create(
            name="Term 1",
            date_from='2024-01-01',
            date_to='2024-05-31',
            active=True
        )
        self.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        
        # Create active and inactive subjects
        self.active_subject = Subject.objects.create(
            name="Subject1",
            active=True
        )
        self.inactive_subject = Subject.objects.create(
            name="Subject2",
            active=False
        )
        
        # Create a ScheduleTemplate instance for edit testing
        self.schedule_template = ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=2,
            order_number=1,
            subject=self.active_subject
        )

    def test_subject_queryset_filters_active_only(self):
        """
        Test that the subject field queryset contains only active subjects.
        """
        form = ScheduleTemplateForm(instance=self.schedule_template)
        subjects_queryset = form.fields['subject'].queryset
        self.assertIn(self.active_subject, subjects_queryset)
        self.assertNotIn(self.inactive_subject, subjects_queryset)

    def test_form_valid_with_all_fields(self):
        """Test form validation for valid data."""
        form_data = {
            'term': self.term.id,
            'study_group': self.study_group.id,
            'weekday': 3,
            'order_number': 1,
            'subject': self.active_subject.id
        }

        form = ScheduleTemplateForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_invalid_without_required_fields(self):
        """Test form validation fails when required fields are missing."""
        form_data = {
            'order_number': 1,
            'subject': ''
        }
        form_initial = {
            'term': self.term.id,
            'study_group': self.study_group.id,
            'weekday': 3,
        }
        form = ScheduleTemplateForm(data=form_data, initial=form_initial)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)


class ScheduleFilterFormTests(TestCase):
    """
    Test suite for ScheduleFilterForm to ensure form fields,
    querysets, and validation behave correctly.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data by creating active and inactive terms 
        and study groups for validating form filtering and field behavior.
        """
        cls.group1 = StudyGroup.objects.create(name="Group A", active=True)
        cls.group2 = StudyGroup.objects.create(name="Group B", active=False)

    def test_form_fields(self):
        """
        Validates that the form includes 'term' and 'study_group' fields 
        and confirms that their labels are correctly set.
        """
        form = ScheduleFilterForm()
        # Check if 'term' and 'study_group' fields are in the form
        self.assertIn('date', form.fields)
        self.assertIn('study_group', form.fields)
        # Verify labels for each field
        self.assertEqual(form.fields['date'].label, "Week Date")
        self.assertEqual(form.fields['study_group'].label, "Study Group")

    def test_queryset_for_study_group_field(self):
        """
        Confirms that the 'study_group' field's queryset includes only active 
        study groups and excludes inactive ones.
        """
        form = ScheduleFilterForm()
        study_groups_queryset = form.fields['study_group'].queryset
        self.assertIn(self.group1, study_groups_queryset)
        self.assertNotIn(self.group2, study_groups_queryset)

    def test_form_is_valid_with_correct_data(self):
        """
        Ensures that the form is valid when provided with data for both 
        'term' and 'study_group' fields.
        """
        test_date = date(2024, 9, 1)
        form_data = {'date': test_date, 'study_group': self.group1.id}
        form = ScheduleFilterForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
        
        # Check the filter parameters
        filter_params = form.get_filter_params()
        expected_week_start = test_date - timedelta(days=test_date.weekday())
        expected_week_end = expected_week_start + timedelta(days=6)
        
        self.assertEqual(filter_params['study_group'], self.group1)
        self.assertEqual(
            filter_params['date__range'],
            (expected_week_start, expected_week_end)
        )

    def test_form_is_invalid_with_missing_data(self):
        """
        Tests that the form is invalid if required fields are missing, 
        such as when only the 'term' field is provided.
        """
        form_data = {'date': date(2024, 9, 1)}
        form = ScheduleFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('study_group', form.errors)

        form_data = {'study_group': self.group1}
        form = ScheduleFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)


class ScheduleFormTests(TestCase):
    """
    Test suite for ScheduleForm to ensure form fields,
    querysets, and validation behave correctly.
    """

    def setUp(self):
        """Create necessary objects for Schedule."""
        self.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        
        # Create active and inactive subjects
        self.active_subject = Subject.objects.create(
            name="Subject1",
            active=True
        )
        self.inactive_subject = Subject.objects.create(
            name="Subject2",
            active=False
        )
        
        # Create a ScheduleTemplate instance for edit testing
        self.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=self.study_group,
            order_number=1,
            subject=self.active_subject,
            homework='homework'
        )

    def test_subject_queryset_filters_active_only(self):
        """
        Test that the subject field queryset contains only active subjects.
        """
        form = ScheduleForm(instance=self.schedule)
        subjects_queryset = form.fields['subject'].queryset
        self.assertIn(self.active_subject, subjects_queryset)
        self.assertNotIn(self.inactive_subject, subjects_queryset)

    def test_form_valid_with_all_fields(self):
        """Test form validation for valid data."""
        form_data = {
            'date': date(2024, 9, 2),
            'study_group': self.study_group.id,
            'order_number': 1,
            'subject': self.active_subject.id
        }

        form = ScheduleForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_invalid_without_required_fields(self):
        """Test form validation fails when required fields are missing."""
        form_data = {
            'order_number': 1,
            'subject': ''
        }
        form_initial = {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id,
        }
        form = ScheduleForm(data=form_data, initial=form_initial)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)


class StudentMarkFormTest(TestCase):
    def setUp(self):
        # Set up a test user to be used as a 'student'
        self.student = User.objects.create_user(
            username='student', password='password')

    def test_form_valid_data(self):
        # Test form with valid data
        form_data = {
            'student': self.student.id,
            'mark': 85
        }
        form = StudentMarkForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "Form should be valid with correct data."
        )

    def test_form_invalid_empty_student(self):
        # Test form with an empty 'student' field
        form_data = {
            'student': None,
            'mark': 85
        }
        form = StudentMarkForm(data=form_data)
        self.assertFalse(
            form.is_valid(),
            "Form should be invalid if 'student' is empty."
        )
        self.assertIn(
            'student',
            form.errors,
            "Expected an error message for the empty 'student' field."
        )

    def test_form_invalid_empty_mark(self):
        # Test form with an empty 'mark' field
        form_data = {
            'student': self.student.id,
            'mark': None
        }
        form = StudentMarkForm(data=form_data)
        self.assertFalse(
            form.is_valid(),
            "Form should be invalid if 'mark' is empty."
        )
        self.assertIn(
            'mark',
            form.errors,
            "Expected an error message for the empty 'mark' field."
        )
