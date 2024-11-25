from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse


class CustomAuthViewTests(TestCase):
    """
    Test case for verifying the custom login and signup views' redirection
    behavior based on user group membership.
    """
    def setUp(self):
        """ Create the data for testing. """
        self.student_group = Group.objects.get(name='Student')
        self.tutor_group = Group.objects.get(name='Tutor')

        # Set up test users
        self.student_user = User.objects.create_user(
            username='student@email.com',
            email='student@email.com',
            password='Password123!',
            first_name='student',
            last_name='student'
        )
        self.tutor_user = User.objects.create_user(
            username='tutor@email.com',
            email='tutor@email.com',
            password='Password123!',
            first_name='tutor',
            last_name='tutor'
        )
        self.user = User.objects.create_user(
            username='user@email.com',
            email='user@email.com',
            password='Password123!',
            first_name='user',
            last_name='user'
        )

        # Assign groups to users
        self.student_user.groups.add(self.student_group)
        self.student_user.save()

        self.tutor_user.groups.add(self.tutor_group)
        self.tutor_user.save()
        # Set up the client for testing
        self.client = Client()

    def test_student_login_redirect(self):
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
        self.assertRedirects(response, reverse('student:dashboard'))

    def test_student_login_redirect(self):
        """
        Test that a tutor user is redirected to the tutor dashboard after
        login.
        """
        response = self.client.post(
            reverse('account_login'),
            {'login': 'tutor@email.com', 'password': 'Password123!'}
        )
        if response.status_code == 200:
            print(response.context['form'].errors)

        # Check for the redirect to student dashboard
        self.assertRedirects(response, reverse('tutor:schedule'))

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

        self.assertRedirects(response, reverse('student:dashboard'))

    def test_user_login_redirect(self):
        """
        Test that a user without groups is redirected to the home page after
        login.
        """
        response = self.client.post(
            reverse('account_login'),
            {'login': 'user@email.com', 'password': 'Password123!'}
        )
        if response.status_code == 200:
            print(response.context['form'].errors)

        # Check for the redirect to student dashboard
        self.assertRedirects(response, reverse('home'))
