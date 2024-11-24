from datetime import date

from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.contrib.auth.models import User, Group
from django.urls import reverse

from dictionaries.models import (
    Term,
    StudyGroup,
    Schedule,
    Subject,
    ScheduleTemplate,
    StudentMark
)
from dictionaries.forms import ScheduleFilterForm, ScheduleForm

from tutor_dashboard.views import ScheduleView, ScheduleBaseView

from users.models import UserProfile


class ScheduleBaseViewTests(TestCase):
    """
    Test suite for the ScheduleBaseView to ensure shared functionality works
    as expected.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data for testing purposes.
        """
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)
        cls.client = Client()
        cls.view = ScheduleBaseView()
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)

    def test_parse_date_with_valid_string(self):
        """
        Test that parse_date correctly converts a valid date string to a date
        object.
        """
        date_string = "2024-11-05"
        parsed_date = self.view.parse_date(date_string)
        self.assertEqual(parsed_date, date(2024, 11, 5))

    def test_parse_date_with_date_object(self):
        """
        Test that parse_date returns the same date object if a date is
        provided.
        """
        parsed_date = self.view.parse_date(date(2024, 11, 5))
        self.assertEqual(parsed_date, date(2024, 11, 5))

    def test_parse_date_with_invalid_string(self):
        """
        Test that parse_date raises a ValueError for an invalid date string.
        """
        invalid_date_string = "invalid-date"
        with self.assertRaises(ValueError):
            self.view.parse_date(invalid_date_string)

    def test_get_initial_data_with_request(self):
        """
        Test that get_initial_data extracts the correct initial data from the
        request.
        """
        self.client.login(username="tutor", password="password")
        request = self.client.get(reverse('tutor:schedule'), {
            'date': '2024-11-05',
            'study_group': self.study_group.id,
            'order_number': 1,
            'subject': self.subject.id
        })
        initial_data = self.view.get_initial_data(request.wsgi_request.GET)
        self.assertEqual(initial_data['date'], date(2024, 11, 5))
        self.assertEqual(initial_data['study_group'], str(self.study_group.id))
        self.assertEqual(initial_data['order_number'], '1')
        self.assertEqual(initial_data['subject'], str(self.subject.id))

    def test_handle_redirect_with_valid_data(self):
        """
        Test that handle_redirect correctly constructs a redirect response with
        the right URL.
        """
        self.client.login(username="tutor", password="password")
        form_data = {
            'date': date(2024, 11, 5),
            'study_group': self.study_group
        }
        response = self.view.handle_redirect(form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = (
            f"{reverse('tutor:schedule')}?date=2024-11-05&study_group=1"
        )

        self.assertEqual(response.url, expected_url)

    def test_handle_redirect_with_invalid_data(self):
        """
        Test that handle_redirect correctly constructs a redirect response with
        the right URL.
        """
        self.client.login(username="tutor", password="password")
        form_data = {
            'study_group': self.study_group
        }
        response = self.view.handle_redirect(form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = (
            f"{reverse('tutor:schedule')}?date=&study_group=1"
        )
        self.assertEqual(response.url, expected_url)

        form_data = {
            'date': date(2024, 11, 5)
        }
        response = self.view.handle_redirect(form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = (
            f"{reverse('tutor:schedule')}?date=2024-11-05&study_group="
        )

        self.assertEqual(response.url, expected_url)


class ScheduleViewTests(TestCase):
    """
    Test suite for the ScheduleView to ensure the GET and POST
    methods, as well as the schedule organization, function as expected.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data for study groups, and subjects.
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
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)
        UserProfile.objects.create(
            user=cls.student_user,
            study_group=cls.study_group,
            checked=True
        )
        cls.student_mark = StudentMark.objects.create(
            schedule=cls.schedule,
            student=cls.student_user,
            mark=95
        )

    def setUp(self):
        """
        Sets up a test client and the URL for the 'schedule' view.
        """
        self.client = Client()
        self.url = reverse('tutor:schedule')

    def test_get_request_renders_template_with_initial_form(self):
        """
        Test that a GET request renders the template with the filter form and
        schedule templates in context.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.get(
            self.url,
            data={
                'date': date(2024, 9, 3),
                'study_group': self.study_group.id
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/schedule.html'
        )

        self.assertIsInstance(
            response.context['form'],
            ScheduleFilterForm
        )
        self.assertEqual(
            response.context['form'].data['date'],
            '2024-09-03'
        )
        self.assertEqual(
            response.context['form'].data['study_group'],
            str(self.study_group.id)
        )

        self.assertIn('schedule', response.context)
        self.assertFalse(response.context['table_empty'])

    def test_student_view_schedule(self):
        """
        Test that a student can view schedule.
        """
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_redirects_with_filter_params(self):
        """
        Test that a POST request with valid form data redirects to the view
        with appropriate query parameters.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id
        })
        expected_url = (
            f"{self.url}?date={date(2024, 9, 3)}&"
            f"study_group={self.study_group.id}"
        )
        self.assertRedirects(response, expected_url)

    def test_post_request_with_invalid_data(self):
        """
        Test that a POST request with invalid data (e.g., missing required
        fields) redirects with only the provided term or study group ID.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {'date': date(2024, 9, 3)})
        expected_url = f"{self.url}?date={date(2024, 9, 3)}&study_group="
        self.assertRedirects(response, expected_url)

    def test_get_schedule_with_valid_ids(self):
        """
        Test get_schedule returns a schedule with templates organized by
        weekday and table_empty=False for valid term and study group IDs.
        """
        view = ScheduleView()
        form_data = {'date': date(2024, 9, 3), 'study_group': self.study_group}
        form = ScheduleFilterForm(
            data=form_data,
            is_student=False,
            user_study_group=self.study_group,
        )
        filter_params = form.get_filter_params()
        schedule, table_empty = view.get_schedule(
            filter_params, {'is_student': False}
        )
        self.assertFalse(table_empty)
        self.assertIn(1, schedule)
        self.assertEqual(schedule[1]['details'][1]['subject'], self.subject)

    def test_unauthorized_user_access(self):
        """
        Test that an unauthorized user (not in Tutor or Student groups)
        cannot access the schedule view.
        """
        unauthorized_user = User.objects.create_user(
            username="unauthorized_user", password="password"
        )
        self.client.login(username="unauthorized_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_request_with_no_schedule(self):
        """
        Test that a valid GET request with no schedule available displays an
        info message.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.get(self.url, {
            'date': date(2024, 9, 10),
            'study_group': self.study_group.id
        })

        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(
            messages_list[0].message,
            "No schedule available for the selected date and study group."
        )

    def test_get_request_with_successful_schedule_display(self):
        """
        Test that a valid GET request displays success messages when schedules
        are found.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.get(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id
        })

        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(
            messages_list[0].message,
            "Schedule displayed successfully.")

    def test_student_redirection(self):
        """
        Test that a student is redirected to the schedule page with the correct
        date when they submit the filter form.
        """

        self.client.login(username="student", password="password")

        post_data = {
            "date": date(2024, 9, 3),
        }
        response = self.client.post(self.url, post_data)

        expected_url = f"{self.url}?date={date(2024, 9, 3)}"
        self.assertRedirects(response, expected_url)

    def test_tutor_redirection(self):
        """
        Test that a tutor is redirected to the schedule page with both date and
        study_group parameters when they submit the filter form.
        """
        self.client.login(username="tutor", password="password")

        post_data = {
            "date": "2024-09-03",
            "study_group": self.study_group.id,
        }
        response = self.client.post(self.url, post_data)
        expected_url = (
            f"{self.url}?date={date(2024, 9, 3)}&"
            f"study_group={self.study_group.id}"
        )
        self.assertRedirects(
            response,
            expected_url
        )

    def test_student_marks_in_schedule(self):
        """
        Test that the student's marks are correctly displayed in the schedule
        when the student is viewing their schedule.
        """
        self.client.login(username="student", password="password")

        get_data = {
            "date": "2024-09-03",
        }

        response = self.client.get(self.url, get_data)

        self.assertIn('schedule', response.context)

        schedule_data = response.context['schedule']
        for day_schedule in schedule_data.values():
            for order, details in day_schedule['details'].items():
                if details['id'] == self.schedule.id:
                    self.assertEqual(details['marks'], 95)


class EditScheduleViewTests(TestCase):
    """
    Test suite for EditScheduleView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for testing.
        """

        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Schedule template instance to be edited
        cls.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=cls.study_group,
            order_number=1,
            subject=cls.subject,
            homework='homework'
        )
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)

    def setUp(self):
        """
        Set up client and URL for the view under test.
        """
        self.client = Client()
        self.url = reverse(
            'tutor:edit_schedule',
            args=[self.schedule.pk]
        )

    def test_get_request_renders_form_with_instance_data(self):
        """
        Test that a GET request renders the form with instance data.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule.html'
        )

        form = response.context['schedule']
        self.assertIsInstance(form, ScheduleForm)
        self.assertEqual(form.instance, self.schedule)

    def test_student_cannot_edit_schedule(self):
        """
        Test that a student cannot edit schedule.
        """
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_request_with_valid_data_updates_instance(self):
        """
        Test that a POST request with valid data updates the Schedule
        instance and redirects correctly.
        """
        new_subject = Subject.objects.create(name="Subject2", active=True)
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.pk,
            'weekday': 1,
            'order_number': 1,
            'subject': new_subject.pk
        })

        # Refresh instance from database and check updated values
        self.schedule.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        expected_url = (
            f"{reverse('tutor:schedule')}?date={date(2024, 9, 3)}&"
            f"study_group={self.study_group.pk}"
        )
        self.assertRedirects(response, expected_url)
        self.assertEqual(self.schedule.subject, new_subject)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Schedule updated successfully.",
            str(messages[0])
        )

    def test_post_request_with_invalid_data_displays_errors(self):
        """
        Test that a POST request with invalid data renders the form with
        errors.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.pk,
            'order_number': '',
            'subject': self.subject.pk
        })
        form = response.context['form']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule.html'
        )
        self.assertFalse(form.is_valid())
        self.assertIn('order_number', form.errors)

        messages = list(get_messages(response.wsgi_request))
        error_messages = [
            f"Error in {field}: {error}"
            for field, errors in form.errors.items()
            for error in errors
        ]
        for error_message in error_messages:
            self.assertTrue(any(
                str(message) == error_message
                for message in messages
            ))


class AddScheduleViewTests(TestCase):
    """Test suite for the AddScheduleView functionality, verifying access,
    data handling, permissions, and messages."""

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for testing:
        - Creates study group, subject, tutor user, and student user.
        - Assigns tutor and student users to appropriate groups.
        """
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)
        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)

    def setUp(self):
        """
        Set up client and URL for the view under test.
        """
        self.client = Client()
        self.url = reverse('tutor:add_schedule')

    def test_get_add_schedule_template_view(self):
        """Test the GET method renders the form with initial data."""
        self.client.login(username="tutor", password="password")
        response = self.client.get(
            self.url,
            {
                'date': date(2024, 9, 3),
                'study_group': self.study_group.id,
                'order_number': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule.html'
        )
        self.assertIsInstance(response.context['schedule'], ScheduleForm)
        self.assertEqual(
            response.context['schedule'].initial['date'],
            date(2024, 9, 3)
        )
        self.assertEqual(
            response.context['schedule'].initial['study_group'],
            str(self.study_group.id)
        )

    def test_get_student_cannot_add_schedule(self):
        """
        Test that a student cannot call GET method.
        """
        self.client.login(username="student", password="password")
        response = self.client.get(
            self.url,
            {
                'date': date(2024, 9, 3),
                'study_group': self.study_group.id,
                'order_number': 1
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_post_add_schedule_view_success(self):
        """Test the POST method successfully adds a Schedule."""
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id,
            'order_number': 1,
            'subject': self.subject.id
        })
        created_schedule = Schedule.objects.get(
            date=date(2024, 9, 3),
            study_group=self.study_group,
            order_number=1,
            subject=self.subject
        )
        self.assertRedirects(
            response,
            reverse('tutor:edit_schedule', args=[created_schedule.pk])
            )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Schedule added successfully.",
            str(messages[0])
        )

    def test_get_student_cannot_add_schedule(self):
        """
        Test that a student cannot call POST method.
        """
        self.client.login(username="student", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id,
            'order_number': 1,
            'subject': self.subject.id
        })
        self.assertEqual(response.status_code, 403)

    def test_post_add_schedule_view_failure(self):
        """Test the POST method fails when form data is invalid."""
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'date': date(2024, 9, 3),
            'study_group': self.study_group.id,
            'order_number': 1,
            'subject': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule.html'
        )
        self.assertFormError(
            response,
            'form',
            'subject',
            'This field is required.'
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Error in subject: This field is required.",
            str(messages[0])
        )


class DeleteScheduleViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data for study groups, and subjects.
        """

        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        cls.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        cls.student_user = User.objects.create_user(
            username="student",
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        cls.tutor_user.groups.add(tutor_group)
        cls.student_user.groups.add(student_group)

    def setUp(self):
        # Create schedule templates
        self.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=self.study_group,
            order_number=1,
            subject=self.subject
        )
        self.client = Client()
        self.url = reverse(
            'tutor:delete_schedule',
            kwargs={'pk': self.schedule.pk}
        )

    def test_delete_schedule_success(self):
        """
        Test that a schedule can be successfully deleted.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url)

        # Check that the schedule was deleted
        self.assertEqual(Schedule.objects.count(), 0)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Schedule deleted successfully.")

        # Check redirect behavior
        expected_url = (
            f"{reverse('tutor:schedule')}?date={self.schedule.date}&"
            f"study_group={self.schedule.study_group.id}"
            )
        self.assertRedirects(response, expected_url)

    def test_delete_schedule_permission_denied(self):
        """
        Test that a user without permission cannot delete a schedule.
        """
        self.client.login(username="student", password="password")

        response = self.client.post(self.url)

        # Check that the schedule still exists
        self.assertEqual(Schedule.objects.count(), 1)

        # Check for permission denied message or the status code
        self.assertEqual(response.status_code, 403)

    def test_delete_schedule_not_found(self):
        """
        Test that a 404 is returned if the schedule does not exist.
        """
        self.client.login(username="tutor", password="password")

        # Attempt to delete a non-existing schedule
        invalid_url = reverse('tutor:delete_schedule', kwargs={'pk': 999})
        response = self.client.post(invalid_url)

        # Check for a 404 response
        self.assertEqual(response.status_code, 404)


class FillScheduleViewTests(TestCase):
    """Test suite for AddScheduleView."""
    def setUp(self):
        """Set up the test environment."""
        self.study_group = StudyGroup.objects.create(
            name="Group A", active=True
            )
        self.subject = Subject.objects.create(name="Subject1", active=True)

        # Create schedule templates
        self.schedule = Schedule.objects.create(
            date=date(2024, 9, 3),
            study_group=self.study_group,
            order_number=1,
            subject=self.subject
        )
        self.term = Term.objects.create(
            name='Term1',
            date_from=date(2024, 10, 1),
            date_to=date(2024, 10, 31),
            active=True
        )
        self.template = ScheduleTemplate.objects.create(
            study_group=self.study_group,
            weekday=2,
            subject=self.subject,
            order_number=1,
            term=self.term
        )
        self.tutor_user = User.objects.create_user(
            username="tutor",
            password="password"
        )
        self.student_user = User.objects.create_user(
            username="student",
            password="password"
        )
        tutor_group = Group.objects.get(name="Tutor")
        student_group = Group.objects.get(name="Student")
        self.tutor_user.groups.add(tutor_group)
        self.student_user.groups.add(student_group)
        self.date = '2024-10-15'

        self.client = Client()
        self.url = reverse('tutor:fill_schedule')

    def test_post_successful_fill_schedule(self):
        """Test successful schedule filling."""
        self.client.login(username='tutor', password='password')
        response = self.client.post(self.url, {
            'study_group': self.study_group.id,
            'date': self.date
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Schedule.objects.filter(study_group=self.study_group).exists()
            )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Schedule filled successfully from template.', messages)

    def test_post_schedule_exists(self):
        """Test when schedule entries already exist."""
        self.client.login(username='tutor', password='password')
        Schedule.objects.create(
            date=date(2024, 10, 15),
            study_group=self.study_group,
            subject=self.subject,
            order_number=1
        )

        response = self.client.post(self.url, {
            'study_group': self.study_group.id,
            'date': self.date
        })

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            'Schedule entries already exist for the specified study group and '
            'date range.',
            messages)

    def test_post_no_active_terms(self):
        """Test when no active terms are found."""
        self.client.login(username='tutor', password='password')
        Term.objects.all().delete()
        response = self.client.post(self.url, {
            'study_group': self.study_group.id,
            'date': self.date
        })

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            'No active terms found for the specified date range.',
            messages
            )

    def test_post_no_template_found(self):
        """Test when no schedule templates are found."""
        self.client.login(username='tutor', password='password')
        ScheduleTemplate.objects.all().delete()

        response = self.client.post(self.url, {
            'study_group': self.study_group.id,
            'date': self.date
        })

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            'No template found for the selected study group and terms.',
            messages
            )

    def test_post_invalid_data(self):
        """Test when study group and date are not specified."""
        self.client.login(username='tutor', password='password')
        response = self.client.post(self.url, {
            'study_group': '',
            'date': ''
        })

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Study group and date are not specified.', messages)

    def test_get_student_cannot_fill_schedule(self):
        """
        Test that a student cannot call POST method.
        """
        self.client.login(username="student", password="password")
        response = self.client.post(self.url, {
            'study_group': self.study_group.id,
            'date': self.date
        })

        self.assertEqual(response.status_code, 403)
