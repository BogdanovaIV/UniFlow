from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from dictionaries.models import Term, StudyGroup, Schedule, Subject
from dictionaries.forms import ScheduleFilterForm, ScheduleForm
from tutor_dashboard.views import ScheduleView


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
        
        cls.study_group = StudyGroup.objects.create(name="Group A", active=True)
        cls.subject = Subject.objects.create(name="Subject1", active=True)
        
        # Create schedule templates
        cls.schedule = Schedule.objects.create(
            date=date(2024,9,3),
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
        # Check the filter form instance
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
        
        # Check the schedule templates and table_empty flag
        self.assertIn('schedule', response.context)
        self.assertFalse(response.context['table_empty'])

    def test_student_view_schedule(self):
        """
        Test that a student cannot view schedule.
        """
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_redirects_with_filter_params(self):
        """
        Test that a POST request with valid form data redirects to the view with
        appropriate query parameters.
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
        form = ScheduleFilterForm(data=form_data)
        
        # Check the filter parameters
        filter_params = form.get_filter_params()
        schedule, table_empty = view.get_schedule(
            filter_params
        )
        self.assertFalse(table_empty)
        self.assertIn(1, schedule)
        self.assertEqual(schedule[1]['details'][1]['subject'], self.subject)



class EditScheduleViewTests(TestCase):
    """
    Test suite for EditScheduleView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for testing.
        """
        
        cls.study_group = StudyGroup.objects.create(name="Group A", active=True)
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
        
        form = response.context['form']
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

    def test_post_request_with_invalid_data_displays_errors(self):
        """
        Test that a POST request with invalid data renders the form with errors.
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

