from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages

from dictionaries.models import StudyGroup, Subject, StudentMark, Schedule
from dictionaries.forms import StudentMarkForm


class StudentMarkViewTests(TestCase):
    """
    Tests for the StudentMark views, including creating, editing, and
    permission checks for StudentMark entries.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all test cases:
        - Create a study group, subject, and schedule.
        - Create users with Tutor and Student roles.
        - Create a tutor and two students.
        """
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Create schedule templates
        cls.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=cls.study_group,
            order_number=1,
            subject=cls.subject
        )
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password",
            first_name="student"
        )
        cls.student_user2 = User.objects.create_user(
            username="student2",
            password="password",
            first_name="student2"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)
        cls.student_user2.groups.add(student_group)

    def setUp(self):
        """
        Sets up the test client, initial StudentMark entry, and the URL for
        the 'edit_student_mark' view.
        """
        self.student_mark = StudentMark.objects.create(
            student=self.student_user, schedule=self.schedule, mark=90)
        self.client = Client()
        self.url = self.url = reverse(
            'tutor:edit_student_mark',
            args=[self.schedule.pk, self.student_mark.pk]
        )

    def test_edit_student_mark_with_permission(self):
        """
        Tests that a tutor with the correct permission can successfully edit
        a StudentMark entry and receives a success message.
        """
        self.client.login(username='tutor', password='password')
        data = {
            'student': self.student_user.pk,
            'mark': 95,
        }

        response = self.client.post(self.url, data)
        self.student_mark.refresh_from_db()

        # Check that the mark was updated
        self.assertEqual(self.student_mark.mark, 95)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Student mark updated successfully."
        )
        self.assertRedirects(
            response,
            reverse('tutor:edit_schedule', args=[self.schedule.pk])
        )

    def test_edit_student_mark_duplicate_error(self):
        """
        Tests that a duplicate error message appears when attempting to edit
        a StudentMark with a student who already has a mark for the same
        schedule.
        """
        self.client.login(username='tutor', password='password')

        StudentMark.objects.create(
            schedule=self.schedule,
            student=self.student_user2,
            mark=75
        )
        data = {
            'student': self.student_user2.pk,
            'mark': 85,
        }

        response = self.client.post(self.url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Mark for student2 already exists for this schedule.",
            str(messages[0])
        )

    def test_edit_student_mark_permission_denied(self):
        """
        Tests that a student without the required permissions receives
        a 403 Forbidden response when attempting to edit a StudentMark.
        """
        self.client.login(username='student', password='password')
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 403)

    def test_form_validation_error(self):
        """
        Test that form validation errors are handled correctly.
        - Validation error messages are displayed.
        - The original StudentMark entry is not updated.
        """
        self.client.login(username='tutor', password='password')
        post_data = {"student": self.student_user.pk}
        response = self.client.post(self.url, post_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Error in mark" in str(message) for message in messages)
        )

        self.student_mark.refresh_from_db()
        self.assertEqual(self.student_mark.student, self.student_user) 
        self.assertEqual(self.student_mark.mark, 90) 

class AddStudentMarkView(TestCase):
    """
    Tests for the AddStudentMark view, including permissions, duplicate
    handling, and success messaging for adding StudentMark entries.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all test cases:
        - Create a study group, subject, and schedule.
        - Create users with Tutor and Student roles.
        - Create a tutor and two students.
        """
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Create schedule templates
        cls.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=cls.study_group,
            order_number=1,
            subject=cls.subject
        )
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password",
            first_name="student"
        )
        cls.student_user2 = User.objects.create_user(
            username="student2",
            password="password",
            first_name="student2"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)
        cls.student_user2.groups.add(student_group)

    def setUp(self):
        """
        Sets up the test client, an initial StudentMark entry, and the URL
        for the 'add_student_mark' view.
        """
        self.student_mark = StudentMark.objects.create(
            student=self.student_user, schedule=self.schedule, mark=90)
        self.client = Client()
        self.url = self.url = reverse(
            'tutor:add_student_mark', args=[self.schedule.pk]
        )

    def test_add_student_mark_with_permission(self):
        """
        Tests that a tutor with the correct permission can successfully add
        a new StudentMark entry and receives a success message.
        """
        self.client.login(username='tutor', password='password')
        data = {
            'student': self.student_user2.pk,
            'mark': 75,
        }

        response = self.client.post(self.url, data)
        new_mark = StudentMark.objects.get(
            schedule=self.schedule,
            student=self.student_user2)

        # Check if the new mark was added
        self.assertEqual(new_mark.mark, 75)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Student mark added successfully.")
        self.assertRedirects(
            response,
            reverse('tutor:edit_schedule', args=[self.schedule.pk])
        )

    def test_add_student_mark_duplicate_error(self):
        """
        Tests that a duplicate error message appears when attempting to add
        a StudentMark entry for a student who already has a mark for the same
        schedule.
        """
        self.client.login(username='tutor', password='password')
        data = {
            'student': self.student_user.pk,
            'mark': 85,
        }

        response = self.client.post(self.url, data)

        # Check for duplicate error message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "A mark for student already exists for this schedule.",
            str(messages[0]))

    def test_edit_student_mark_permission_denied(self):
        """
        Tests that a student without the required permissions receives
        a 403 Forbidden response when attempting to add a StudentMark.
        """
        self.client.login(username='student', password='password')
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 403)

    def test_form_validation_error_message(self):
        """
        Test that form validation errors are correctly displayed when the form
        data is incomplete or invalid.
        For example, missing required fields should trigger validation
        error messages.
        """
        self.client.login(username='tutor', password='password')
        data = {
            "student": self.student_user.pk,
        }
        response = self.client.post(self.url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Error in" in str(message) for message in messages)
        )
        self.assertEqual(response.status_code, 302)

class DeleteStudentMarkView(TestCase):
    """
    Tests for the DeleteStudentMark view, including permissions and success
    messaging for deleting StudentMark entries.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all test cases:
        - Create a study group, subject, and schedule.
        - Create users with Tutor and Student roles.
        - Create a tutor and two students.
        """
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Create schedule templates
        cls.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=cls.study_group,
            order_number=1,
            subject=cls.subject
        )
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password",
            first_name="student"
        )
        cls.student_user2 = User.objects.create_user(
            username="student2",
            password="password",
            first_name="student2"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)
        cls.student_user2.groups.add(student_group)

    def setUp(self):
        """
        Sets up the test client, an initial StudentMark entry, and the URL for
        the 'delete_student_mark' view.
        """
        self.student_mark = StudentMark.objects.create(
            student=self.student_user, schedule=self.schedule, mark=90)
        self.client = Client()
        self.url = self.url = reverse(
            'tutor:delete_student_mark',
            args=[self.schedule.pk, self.student_mark.pk]
        )

    def test_delete_student_mark_with_permission(self):
        """
        Tests that a tutor with the correct permission can successfully delete
        a StudentMark entry and receives a success message.
        """
        self.client.login(username='tutor', password='password')

        response = self.client.post(self.url)

        # Check if the mark was deleted
        with self.assertRaises(StudentMark.DoesNotExist):
            StudentMark.objects.get(pk=self.student_mark.pk)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Student mark deleted successfully."
        )
        self.assertRedirects(
            response,
            reverse('tutor:edit_schedule', args=[self.schedule.pk])
        )

    def test_delete_student_mark_permission_denied(self):
        """
        Tests that a student without the required permissions receives
        a 403 Forbidden response when attempting to delete a StudentMark entry.
        """
        self.client.login(username='student', password='password')
        response = self.client.post(self.url)

        # Ensure the object still exists
        self.assertTrue(
            StudentMark.objects.filter(pk=self.student_mark.pk).exists()
        )
        self.assertEqual(response.status_code, 403)
