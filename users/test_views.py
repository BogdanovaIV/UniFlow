from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.test import Client


class CustomAuthViewTests(TestCase):
    """
    Test case for verifying the custom login and signup views' redirection
    behavior based on user group membership.
    """
    def setUp(self):
        # Set up groups
        self.student_group = Group.objects.get(name='Student')

        # Set up test users
        self.student_user = User.objects.create_user(
            username='student@email.com',
            email='student@email.com',
            password='Password123!',
            first_name='student',
            last_name='student'
        )

        # Assign groups to users
        self.student_user.groups.add(self.student_group)
        self.student_user.save()
        # Set up the client for testing
        self.client = Client()


    def test_student_login_redirect(self):
        """
        Test that a student user is redirected to the student dashboard after
        login.
        """
        """
        Test that a student user is redirected to the student dashboard after
        login.
        """
        response = self.client.post(
            reverse('account_login'),
            {'login': 'student@email.com', 'password': 'Password123!'}
        )
        if response.status_code == 200:
            print(response.context['form'].errors)
        
        # Check for the redirect to student dashboard
        self.assertRedirects(response, reverse('student_dashboard'))


    def test_student_signup_redirect(self):
        """
        Test that a student user is redirected to the student dashboard after
        signup.
        """
        response = self.client.post(reverse('account_signup'), {
            'email': 'new_student@email.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'first_name': 'New',
            'last_name': 'Student'
        })

        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertRedirects(response, reverse('student_dashboard'))

