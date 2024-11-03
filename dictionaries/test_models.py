from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    StudyGroup,
    Term,
    Subject,
    WeekdayChoices,
    ScheduleTemplate,
    Schedule,
    StudentMark
    )



class TestStudyGroupModel(TestCase):
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
        """
        Test that creating a StudyGroup with a duplicate name raises
        an IntegrityError.
        """
        StudyGroup.objects.create(name="102", active=True)
        with self.assertRaises(Exception):
            StudyGroup.objects.create(name="102", active=False)

    def test_active_default(self):
        """Test that the active field defaults to True."""
        new_group = StudyGroup.objects.create(name="103")
        self.assertTrue(new_group.active)


class TestTermModelTest(TestCase):
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
            "2024-2025 Term 1"
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


class TestSubjectModel(TestCase):
    """
    Test cases for the Subject model.
    """

    def setUp(self):
        # Create a Subject instance
        self.subject = StudyGroup.objects.create(name="subject1", active=True)

    def test_str_representation(self):
        """Test the string representation of Subject."""
        self.assertEqual(str(self.subject), "subject1")
    
    def subject_name_cannot_be_empty(self):
        """
        Test if a subject cannot be created with an empty name.
        """
        subject = Subject(name='', active=True)
        with self.assertRaises(ValidationError):
            subject.full_clean()  # This will trigger validation

    def test_unique_name(self):
        """
        Test that creating a Subject with a duplicate name raises
        an IntegrityError.
        """
        Subject.objects.create(name="subject2", active=True)
        with self.assertRaises(Exception):
            Subject.objects.create(name="subject2", active=False)

    def test_active_default(self):
        """Test that the active field defaults to True."""
        new_subject = Subject.objects.create(name="subject3")
        self.assertTrue(new_subject.active)


class WeekdayChoicesTests(TestCase):
    """
    Tests for the WeekdayChoices IntegerChoices class.
    Verifies the labels and values for each choice in WeekdayChoices.
    """
    
    def test_weekday_choices(self):
        """Test that each choice in WeekdayChoices has the correct label."""
        self.assertEqual(WeekdayChoices.MONDAY.label, 'Monday')
        self.assertEqual(WeekdayChoices.TUESDAY.label, 'Tuesday')
        self.assertEqual(WeekdayChoices.WEDNESDAY.label, 'Wednesday')
        self.assertEqual(WeekdayChoices.THURSDAY.label, 'Thursday')
        self.assertEqual(WeekdayChoices.FRIDAY.label, 'Friday')
        self.assertEqual(WeekdayChoices.SATURDAY.label, 'Saturday')
        self.assertEqual(WeekdayChoices.SUNDAY.label, 'Sunday')

    def test_weekday_choices_values(self):
        """
        Test that each choice in WeekdayChoices has the correct integer value.
        """
        self.assertEqual(WeekdayChoices.MONDAY.value, 0)
        self.assertEqual(WeekdayChoices.TUESDAY.value, 1)
        self.assertEqual(WeekdayChoices.WEDNESDAY.value, 2)
        self.assertEqual(WeekdayChoices.THURSDAY.value, 3)
        self.assertEqual(WeekdayChoices.FRIDAY.value, 4)
        self.assertEqual(WeekdayChoices.SATURDAY.value, 5)
        self.assertEqual(WeekdayChoices.SUNDAY.value, 6)


class ScheduleTemplateTests(TestCase):
    """
    Tests for the ScheduleTemplate model.
    Covers model field validation, unique constraints, and string representation.
    """

    def setUp(self):
        """Set up test instances for foreign key fields."""
        self.term = Term.objects.create(
            name='2024-2025 term 1',
            date_from='2024-01-01',
            date_to='2024-05-31',
            active=True
        )
        self.study_group = StudyGroup.objects.create(
            name='101',
            active=True
        )
        self.subject = Subject.objects.create(name='Subject1', active=True)

    def test_schedule_template_creation(self):
        """
        Test that a ScheduleTemplate instance can be created with valid fields.
        """
        schedule = ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        self.assertEqual(schedule.term, self.term)
        self.assertEqual(schedule.study_group, self.study_group)
        self.assertEqual(schedule.weekday, int(WeekdayChoices.MONDAY))
        self.assertEqual(schedule.order_number, 1)
        self.assertEqual(schedule.subject, self.subject)

    def test_schedule_template_str_method(self):
        """
        Test the __str__ method returns the correct string representation.
        """
        schedule = ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        expected_str = (
            f"{self.term} - "
            f"{self.study_group} - "
            f"{WeekdayChoices.MONDAY} - "
            "1. - "
            f"{self.subject}"
        )
        
        self.assertEqual(str(schedule), expected_str)

    def test_order_number_validation(self):
        """
        Test that order_number raises ValidationError when outside the valid
        range (1-10).
        """
        schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=11,  # Out of range
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

        schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=0,  # Out of range
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_unique_constraint(self):
        """Test that a unique constraint violation raises a ValidationError."""
        # Create a ScheduleTemplate instance
        ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        # Attempt to create a duplicate entry
        duplicate_schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            duplicate_schedule.full_clean()  # Trigger unique constraint error

    def test_term_field_null(self):
        """
        Test that the term field cannot be null.
        """
        schedule = ScheduleTemplate(
            term=None,  # Invalid
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_study_group_field_null(self):
        """
        Test that the study_group field cannot be null.
        """
        schedule = ScheduleTemplate(
            term=self.term,
            study_group=None,  # Invalid
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_weekday_field_null(self):
        """
        Test that the weekday field cannot be null.
        """
        schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=None,  # Invalid
            order_number=1,
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_order_number_field_null(self):
        """
        Test that the order_number field cannot be null.
        """
        schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=None,  # Invalid
            subject=self.subject
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_subject_field_null(self):
        """
        Test that the subject field cannot be null.
        """
        schedule = ScheduleTemplate(
            term=self.term,
            study_group=self.study_group,
            weekday=WeekdayChoices.MONDAY,
            order_number=1,
            subject=None  # Invalid
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error


class ScheduleTests(TestCase):
    """
    Tests for the Schedule model.
    Covers model field validation, unique constraints, and string
    representation.
    """

    def setUp(self):
        """Set up test instances for foreign key fields."""
        self.study_group = StudyGroup.objects.create(
            name='101',
            active=True
        )
        self.subject = Subject.objects.create(name='Subject1', active=True)

    def test_schedule_creation(self):
        """
        Test that a Schedule instance can be created with valid fields.
        """
        schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )

        self.assertEqual(schedule.study_group, self.study_group)
        self.assertEqual(schedule.date, date(2024, 9, 1))
        self.assertEqual(schedule.order_number, 1)
        self.assertEqual(schedule.subject, self.subject)
        self.assertEqual(schedule.homework, 'Homework')

    def test_schedule_str_method(self):
        """
        Test the __str__ method returns the correct string representation.
        """
        schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )
        
        expected_str = (
            f"{self.study_group} - "
            f"{schedule.date} - "
            "1. - "
            f"{self.subject}"
        )
        
        self.assertEqual(str(schedule), expected_str)

    def test_order_number_validation(self):
        """
        Test that order_number raises ValidationError when outside the valid
        range (1-10).
        """
        schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=11,  # Out of range
            subject=self.subject,
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

        schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=0,  # Out of range
            subject=self.subject,
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_unique_constraint(self):
        """Test that a unique constraint violation raises a ValidationError."""
        # Create a Schedule instance
        schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )
        
        # Attempt to create a duplicate entry
        with self.assertRaises(ValidationError):
            duplicate_schedule = Schedule(
                study_group=self.study_group,
                date=date(2024, 9, 1),
                order_number=1,
                subject=self.subject,
                homework='Homework'
            )
            duplicate_schedule.full_clean()  # This should raise a ValidationError

    def test_study_group_field_null(self):
        """
        Test that the study_group field cannot be null.
        """
        schedule = Schedule(
            study_group=None,  # Invalid
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_date_field_null(self):
        """
        Test that the date field cannot be null.
        """
        schedule = Schedule(
            study_group=self.study_group,
            date=None, # Invalid
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_order_number_field_null(self):
        """
        Test that the order_number field cannot be null.
        """
        schedule = Schedule(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=None,  # Invalid
            subject=self.subject,
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_subject_field_null(self):
        """
        Test that the subject field cannot be null.
        """
        schedule = Schedule(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=None,  # Invalid
            homework='Homework'
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()  # Trigger validation error

    def test_homework_field_null(self):
        """
        Test that the subject field can be null.
        """
        schedule = Schedule(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject
        )
        try:
            schedule.full_clean()  # Trigger validation to check for errors
        except ValidationError as e:
            self.fail(
                f"Schedule.full_clean() raised ValidationError "
                f"unexpectedly: {e}"
            )


class StudentMarkModelTests(TestCase):
   
    def setUp(self):
        """Set up test instances for foreign key fields."""
        self.student = User.objects.create_user(
            username='student', password='password'
            )
        self.study_group = StudyGroup.objects.create(
            name='101',
            active=True
        )
        self.subject = Subject.objects.create(name='Subject1', active=True)
        self.schedule = Schedule.objects.create(
            study_group=self.study_group,
            date=date(2024, 9, 1),
            order_number=1,
            subject=self.subject,
            homework='Homework'
        )

    def test_create_student_mark(self):
        """Test creating a StudentMark with valid data."""
        student_mark = StudentMark.objects.create(
            student=self.student,
            schedule=self.schedule,
            mark=85
        )
        self.assertEqual(student_mark.mark, 85)
        self.assertEqual(student_mark.student, self.student)
        self.assertEqual(student_mark.schedule, self.schedule)

    def test_mark_within_valid_range(self):
        """Test that the mark value is within the valid range (0-100)."""
        student_mark = StudentMark(student=self.student, schedule=self.schedule)

        # Test valid marks
        student_mark.mark = 0
        student_mark.full_clean()

        student_mark.mark = 100
        student_mark.full_clean()

    def test_mark_out_of_range(self):
        """Test that a ValidationError is raised if the mark is out of range."""
        student_mark = StudentMark(student=self.student, schedule=self.schedule)

        # Test mark below 0
        student_mark.mark = -1
        with self.assertRaises(ValidationError):
            student_mark.full_clean()

        # Test mark above 100
        student_mark.mark = 101
        with self.assertRaises(ValidationError):
            student_mark.full_clean()

    def test_unique_constraint(self):
        """Test unique constraint on schedule and student."""
        # Create initial StudentMark instance
        StudentMark.objects.create(
            student=self.student,
            schedule=self.schedule,
            mark=75
            )

        # Attempt to create another with the same schedule and student
        duplicate_student_mark = StudentMark(
            student=self.student,
            schedule=self.schedule,
            mark=85
            )
        with self.assertRaises(ValidationError):
            duplicate_student_mark.full_clean()

    def test_string_representation(self):
        """Test the string representation of the StudentMark instance."""
        student_mark = StudentMark.objects.create(
            student=self.student,
            schedule=self.schedule,
            mark=90
        )
        self.assertEqual(
            str(student_mark),
            f"{self.schedule} - {self.student} - 90"
        )