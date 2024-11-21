from django.test import TestCase, RequestFactory
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from users.forms import CustomSignupForm


class TestCustomSignupForm(TestCase):
    """Test cases for the CustomSignupForm."""

    def setUp(self):
        """Set up initial data for testing."""
        self.valid_data = {
            'email': 'testuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'first_name': 'Test',
            'last_name': 'User',
        }

        self.invalid_data_first_name = {
            'email': 'testuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'first_name': '',  # Invalid: empty
            'last_name': 'User',
        }

        self.invalid_data_last_name = {
            'email': 'testuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'first_name': 'Test',
            'last_name': '',  # Invalid: empty
        }

        self.factory = RequestFactory()

    def test_valid_form(self):
        """Test that the form is valid with all required fields."""
        # Create a mock request
        request = self.factory.post('/accounts/signup/', data=self.valid_data)

        # Manually set up the session
        session = SessionStore()
        request.session = session

        form = CustomSignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save(request)  # Pass the request object
        self.assertEqual(user.username, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])

    def test_invalid_form_first_name(self):
        """Test that the form is invalid with missing first name."""
        form = CustomSignupForm(data=self.invalid_data_first_name)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_invalid_form_last_name(self):
        """Test that the form is invalid with missing last name."""
        form = CustomSignupForm(data=self.invalid_data_last_name)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
