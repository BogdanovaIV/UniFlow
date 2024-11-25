from datetime import date

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.urls import reverse

from dictionaries.models import Term, StudyGroup, ScheduleTemplate, Subject
from dictionaries.forms import (
    ScheduleTemplateFilterForm,
    ScheduleTemplateForm
)

from tutor_dashboard.views import (
    ScheduleTemplateView,
    ScheduleTemplateBaseView
)


class ScheduleTemplateBaseViewTests(TestCase):
    """
    Test suite for ScheduleTemplateBaseView, covering initial data extraction
    and redirection handling.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the test case, including creating a term and study
        group.
        """
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
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
        """ Set up the request factory and view instance for each test. """
        self.client = Client()
        self.view = ScheduleTemplateBaseView()

    def test_get_initial_data_with_valid_get_parameters(self):
        """
        Test that get_initial_data retrieves correct initial data with valid
        GET parameters.
        """

        self.client.login(username="tutor", password="password")
        request = self.client.get(reverse('tutor:schedule_templates'), {
            'term': str(self.term.id),
            'study_group': str(self.study_group.id),
            'weekday': '1',
            'order_number': '1'
        })
        initial_data = self.view.get_initial_data(request.wsgi_request.GET)

        self.assertEqual(initial_data['term'], str(self.term.id))
        self.assertEqual(initial_data['study_group'], str(self.study_group.id))
        self.assertEqual(initial_data['weekday'], '1')
        self.assertEqual(initial_data['order_number'], '1')

    def test_get_initial_data_with_missing_get_parameters(self):
        """
        Test that get_initial_data correctly sets missing parameters to None.
        """
        self.client.login(username="tutor", password="password")
        request = self.client.get(reverse('tutor:schedule_templates'), {
            'term': str(self.term.id)
        })
        initial_data = self.view.get_initial_data(request.wsgi_request.GET)

        self.assertEqual(initial_data['term'], str(self.term.id))
        self.assertIsNone(initial_data['study_group'])
        self.assertIsNone(initial_data['weekday'])
        self.assertIsNone(initial_data['order_number'])

    def test_handle_redirect_with_valid_form_data(self):
        """
        Test that handle_redirect redirects to the expected URL with form data.
        """
        data = {'term': self.term, 'study_group': self.study_group}

        response = self.view.handle_redirect(data)

        # Expected redirect URL
        expected_url = (
            f"{reverse('tutor:schedule_templates')}?term={self.term.id}"
            f"&study_group={self.study_group.id}"
        )

        # Verify the redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test_get_initial_data_with_empty_get_parameters(self):
        """
        Test that get_initial_data handles empty GET parameters by setting all
        fields to None.
        """
        self.client.login(username="tutor", password="password")
        request = self.client.get(reverse('tutor:schedule_templates'))
        initial_data = self.view.get_initial_data(request.wsgi_request.GET)

        self.assertIsNone(initial_data['term'])
        self.assertIsNone(initial_data['study_group'])
        self.assertIsNone(initial_data['weekday'])
        self.assertIsNone(initial_data['order_number'])


class ScheduleTemplateViewTests(TestCase):
    """
    Test suite for the ScheduleTemplateView to ensure the GET and POST
    methods, as well as the schedule organization, function as expected.
    """
    @classmethod
    def setUpTestData(cls):
        """Sets up initial test data for terms, study groups, and subjects."""
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Create schedule templates
        cls.schedule_template = ScheduleTemplate.objects.create(
            term=cls.term,
            study_group=cls.study_group,
            weekday=1,
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
        Sets up a test client and the URL for the 'schedule_templates' view.
        """
        self.client = Client()
        self.url = reverse('tutor:schedule_templates')

    def test_get_request_renders_template_with_initial_form(self):
        """
        Test that a GET request renders the template with the filter form and
        schedule templates in context.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.get(
            self.url,
            {'term': self.term.id, 'study_group': self.study_group.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/schedule_templates.html'
        )

        # Check the filter form instance
        self.assertIsInstance(
            response.context['form'],
            ScheduleTemplateFilterForm
        )
        self.assertEqual(
            response.context['form'].data['term'],
            str(self.term.id)
        )
        self.assertEqual(
            response.context['form'].data['study_group'],
            str(self.study_group.id)
        )

        # Check the schedule templates and table_empty flag
        self.assertIn('schedule_templates', response.context)
        self.assertFalse(response.context['table_empty'])
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Schedule template displayed successfully.",
            str(messages_list[0])
        )

    def test_student_cannot_view_schedule_templates(self):
        """ Test that a student cannot view schedule templates. """
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_request_redirects_with_filter_params(self):
        """
        Test that a POST request with valid form data redirects to the view
        with appropriate query parameters.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'term': self.term.id,
            'study_group': self.study_group.id
        })
        expected_url = (
            f"{self.url}?term={self.term.id}&study_group={self.study_group.id}"
        )
        self.assertRedirects(response, expected_url)

    def test_post_request_with_invalid_data(self):
        """
        Test that a POST request with invalid data (e.g., missing required
        fields) redirects with only the provided term or study group ID.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {'term': self.term.id})
        expected_url = f"{self.url}?term={self.term.id}&study_group="
        self.assertRedirects(response, expected_url)

    def test_get_schedule_templates_with_valid_ids(self):
        """
        Test get_schedule_templates returns a schedule with templates organized
        by weekday and table_empty=False for valid term and study group IDs.
        """
        view = ScheduleTemplateView()
        schedule_templates, table_empty = view.get_schedule_templates(
            self.term.id,
            self.study_group.id
        )

        self.assertFalse(table_empty)
        self.assertIn(1, schedule_templates)
        self.assertEqual(schedule_templates[1][1][1]['subject'], self.subject)

    def test_get_schedule_templates_with_empty_ids(self):
        """
        Test get_schedule_templates returns an empty schedule and
        table_empty=True when term and study group IDs are missing.
        """
        view = ScheduleTemplateView()
        schedule_templates, table_empty = view.get_schedule_templates(
            None,
            None
        )

        self.assertTrue(table_empty)
        self.assertEqual(
            schedule_templates,
            view.get_full_week_schedule(ScheduleTemplate.objects.none())
        )

    def test_get_full_week_schedule(self):
        """
        Test that get_full_week_schedule organizes schedule templates correctly
        by weekday, with empty slots where no template is set.
        """
        view = ScheduleTemplateView()
        schedule = view.get_full_week_schedule(ScheduleTemplate.objects.all())

        # Check that weekday=1 contains the subject in order_number=1
        self.assertEqual(schedule[1][1][1]['subject'], self.subject)
        self.assertEqual(schedule[1][1][1]['id'], self.schedule_template.id)

        # Verify that other slots are empty
        for weekday, (_, orders) in schedule.items():
            for order in range(1, 11):
                if not (weekday == 1 and order == 1):
                    self.assertEqual(orders[order], {'subject': '', 'id': ''})

    def test_get_full_week_schedule_with_no_templates(self):
        """
        Test that get_full_week_schedule returns a fully empty schedule when no
        templates are provided.
        """
        view = ScheduleTemplateView()
        schedule = view.get_full_week_schedule(ScheduleTemplate.objects.none())

        for weekday, (_, orders) in schedule.items():
            for order in range(1, 11):
                self.assertEqual(orders[order], {'subject': '', 'id': ''})


class EditScheduleTemplateViewTests(TestCase):
    """ Test suite for EditScheduleTemplateView. """

    @classmethod
    def setUpTestData(cls):
        """ Set up initial data for testing. """
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        cls.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        cls.subject = Subject.objects.create(name="Subject1", active=True)

        # Schedule template instance to be edited
        cls.schedule_template = ScheduleTemplate.objects.create(
            term=cls.term,
            study_group=cls.study_group,
            weekday=1,
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
        """ Set up client and URL for the view under test. """
        self.client = Client()
        self.url = reverse(
            'tutor:edit_schedule_template',
            args=[self.schedule_template.pk]
        )

    def test_get_request_renders_form_with_instance_data(self):
        """ Test that a GET request renders the form with instance data. """
        self.client.login(username="tutor", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
        )

        form = response.context['form']
        self.assertIsInstance(form, ScheduleTemplateForm)
        self.assertEqual(form.instance, self.schedule_template)

    def test_student_cannot_edit_schedule_templates(self):
        """ Test that a student cannot edit schedule templates. """
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_request_with_valid_data_updates_instance(self):
        """
        Test that a POST request with valid data updates the ScheduleTemplate
        instance and redirects correctly.
        """
        new_subject = Subject.objects.create(name="Subject2", active=True)
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'term': self.term.pk,
            'study_group': self.study_group.pk,
            'weekday': 1,
            'order_number': 1,
            'subject': new_subject.pk
        })

        # Refresh instance from database and check updated values
        self.schedule_template.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        expected_url = (
            f"{reverse('tutor:schedule_templates')}?term={self.term.pk}&"
            f"study_group={self.study_group.pk}"
        )
        self.assertRedirects(response, expected_url)
        self.assertEqual(self.schedule_template.subject, new_subject)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            messages[0].message,
            "Schedule template updated successfully."
        )

    def test_post_request_with_invalid_data_displays_errors(self):
        """
        Test that a POST request with invalid data renders the form with
        errors.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'term': self.term.pk,
            'study_group': self.study_group.pk,
            'weekday': 1,
            'order_number': '',
            'subject': self.subject.pk
        })
        form = response.context['form']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
        )
        self.assertFalse(form.is_valid())
        self.assertIn('order_number', form.errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Error in order_number" in message.message
                for message in messages)
        )


class AddScheduleTemplateViewTests(TestCase):
    """ Test suite for AddScheduleTemplateView. """

    @classmethod
    def setUpTestData(cls):
        """ Set up initial data for testing. """
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
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
        """ Set up client and URL for the view under test. """
        self.client = Client()
        self.url = reverse('tutor:add_schedule_template')

    def test_get_add_schedule_template_view(self):
        """ Test the GET method renders the form with initial data. """
        self.client.login(username="tutor", password="password")
        response = self.client.get(
            self.url,
            {
                'term': self.term.id,
                'study_group': self.study_group.id,
                'weekday': 1,
                'order_number': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
        )
        self.assertIsInstance(response.context['form'], ScheduleTemplateForm)
        self.assertEqual(
            response.context['form'].initial['term'],
            str(self.term.id)
        )
        self.assertEqual(
            response.context['form'].initial['study_group'],
            str(self.study_group.id)
        )

    def test_get_student_cannot_add_schedule_templates(self):
        """ Test that a student cannot call GET method. """
        self.client.login(username="student", password="password")
        response = self.client.get(
            self.url,
            {
                'term': self.term.id,
                'study_group': self.study_group.id,
                'weekday': 1,
                'order_number': 1
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_post_add_schedule_template_view_success(self):
        """ Test the POST method successfully adds a ScheduleTemplate. """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'term': self.term.id,
            'term_id': self.term.id,
            'study_group': self.study_group.id,
            'weekday': 1,
            'order_number': 1,
            'subject': self.subject.id
        })
        self.assertRedirects(
            response,
            f"{reverse('tutor:schedule_templates')}?term={self.term.id}"
            f"&study_group={self.study_group.id}"
            )
        self.assertTrue(
            ScheduleTemplate.objects.filter(
                term=self.term,
                study_group=self.study_group,
                weekday=1,
                order_number=1
            ).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Schedule template added successfully.",
            str(messages[0])
        )

    def test_post_add_schedule_template_view_failure(self):
        """ Test the POST method fails when form data is invalid. """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url, {
            'term': self.term.id,
            'study_group': self.study_group.id,
            'weekday': 1,
            'order_number': 1,
            'subject': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
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


class DeleteScheduleTemplateViewTests(TestCase):
    """ Tests for the DeleteScheduleTemplateView. """
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for testing.
        """
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
        """ Set up test data for the tests. """
        self.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        self.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        self.subject = Subject.objects.create(name="Subject1", active=True)
        self.schedule_template = ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=1,
            order_number=1,
            subject=self.subject
        )
        self.url = reverse(
            'tutor:delete_schedule_template',
            args=[self.schedule_template.pk]
        )

    def test_delete_schedule_template_success(self):
        """ Test successful deletion of a schedule template. """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ScheduleTemplate.objects.filter(
                pk=self.schedule_template.pk
                ).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Schedule template deleted successfully."
        )

    def test_get_student_cannot_add_schedule_templates(self):
        """ Test that a student cannot delete schedule template. """
        self.client.login(username="student", password="password")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_non_existent_schedule_template(self):
        """
        Test trying to delete a non-existent schedule template raises a 404.
        """
        self.client.login(username="tutor", password="password")
        non_existent_url = reverse(
            'tutor:delete_schedule_template',
            args=[999]
        )
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_delete(self):
        """
        Test that the user is redirected to the schedule templates list
        after deletion.
        """
        self.client.login(username="tutor", password="password")
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            f"{reverse('tutor:schedule_templates')}?term={self.term.id}"
            f"&study_group={self.study_group.id}"
            )
