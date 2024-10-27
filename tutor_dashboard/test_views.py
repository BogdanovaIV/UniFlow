from django.test import TestCase, Client
from django.urls import reverse
from dictionaries.models import Term, StudyGroup, ScheduleTemplate, Subject
from dictionaries.forms import ScheduleTemplateFilterForm
from dictionaries.forms import ScheduleTemplateForm
from .views import ScheduleTemplateView
from datetime import date

class ScheduleTemplateViewTests(TestCase):
    """
    Test suite for the ScheduleTemplateView to ensure the GET and POST
    methods, as well as the schedule organization, function as expected.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data for terms, study groups, and subjects.
        """
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        cls.study_group = StudyGroup.objects.create(name="Group A", active=True)
        cls.subject = Subject.objects.create(name="Subject1", active=True)
        
        # Create schedule templates
        cls.schedule_template = ScheduleTemplate.objects.create(
            term=cls.term,
            study_group=cls.study_group,
            weekday=1,  # Monday
            order_number=1,
            subject=cls.subject
        )
        
    def setUp(self):
        """
        Sets up a test client and the URL for the 'schedule_templates' view.
        """
        self.client = Client()
        self.url = reverse('tutor:schedule_templates')

    def test_get_request_renders_template(self):
        """
        Tests that a GET request renders the correct template with an empty form 
        and a full week's schedule structure.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/schedule-templates.html'
        )
        self.assertIsInstance(
            response.context['form'],
            ScheduleTemplateFilterForm
        )
        self.assertIn('schedule_templates', response.context)

    def test_post_request_with_valid_data(self):
        """
        Tests that a POST request with valid form data filters and renders 
        the correct schedule templates.
        """
        response = self.client.post(self.url, {
            'term': self.term.id,
            'study_group': self.study_group.id,
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse(
                'tutor:schedule_templates'
                )}?term={self.term.id}&study_group={self.study_group.id}")
        

    def test_post_request_with_invalid_data(self):
        """
        Tests that a POST request with invalid data (e.g., missing fields)
        re-renders the form with errors.
        """
        response = self.client.post(
            self.url,
            {'term': self.term.id, 'study_group': ''}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse(
                'tutor:schedule_templates'
                )}?term={self.term.id}&study_group=")

    def test_get_full_week_schedule(self):
        """
        Tests that get_full_week_schedule correctly organizes templates by
        weekday and order, including placeholders for empty slots.
        """
        view = ScheduleTemplateView()
        schedule = view.get_full_week_schedule(ScheduleTemplate.objects.all())
        
        # Check that Monday, order 1 contains the subject
        self.assertEqual(
            schedule[1][1][1],
            {'subject': self.subject, 'id': self.subject.id}
        )
        
        # Verify placeholders for other weekdays and orders
        for weekday, (_, orders) in schedule.items():
            for order in range(1, 11):
                if not (weekday == 1 and order == 1):
                    self.assertEqual(orders[order], {'subject': '', 'id': ''})


class EditScheduleTemplateViewTests(TestCase):
    """
    Tests for the EditScheduleTemplateView, covering GET and POST requests with
    valid and invalid data for ScheduleTemplate editing.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up initial test data for terms, study groups, and subjects.
        """
        cls.term = Term.objects.create(
            name="Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        cls.study_group = StudyGroup.objects.create(name="Group A", active=True)
        cls.subject = Subject.objects.create(name="Subject1", active=True)
        
        # Create schedule templates
        cls.schedule_template = ScheduleTemplate.objects.create(
            term=cls.term,
            study_group=cls.study_group,
            weekday=1,  # Monday
            order_number=1,
            subject=cls.subject
        )
        
    def setUp(self):
        """
        Sets up a test client and the URL for the 'schedule_templates' view.
        """
        self.client = Client()
        self.url = reverse(
            'tutor:edit_schedule_template',
            args=[self.schedule_template.pk]
        )

    def test_get_request_renders_form_with_instance_data(self):
        """Test GET request renders form with pre-filled instance data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
        )
        self.assertIsInstance(
            response.context['form'],
            ScheduleTemplateForm
        )
        self.assertEqual(
            response.context['form'].instance,
            self.schedule_template
        )
        
    def test_post_request_valid_data_redirects_to_schedule_template(self):
        """Test POST request with valid data saves form and redirects."""
        updated_subject = Subject.objects.create(name="Physics", active=True)
        response = self.client.post(self.url, {
            'term': self.term.pk,
            'study_group': self.study_group.pk,
            'weekday': 1,
            'subject': updated_subject.pk
        })
        self.schedule_template.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('tutor:schedule_templates')}?term={self.term.pk}"
            f"&study_group={self.study_group.pk}"
        )
        self.assertEqual(self.schedule_template.subject, updated_subject)
    
    def test_post_request_invalid_data_renders_form_with_errors(self):
        """Test POST request with invalid data reloads form with errors."""
        response = self.client.post(self.url, {
            'term': self.term.pk,
            'study_group': self.study_group.pk,
            'weekday': 1,
            'subject': ''
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'tutor_dashboard/edit_schedule_template.html'
        )
        self.assertIsInstance(response.context['form'], ScheduleTemplateForm)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('subject', response.context['form'].errors)