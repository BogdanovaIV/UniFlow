from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    """ Test cases for the Home page of the application. """

    def test_home_page_status_code(self):
        """ Test if the home page returns a 200 status code. """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """ Test if the home page uses the correct template. """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_home_page_contains_correct_html(self):
        """ Test if the home page contains specific text. """
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Medical University')

    def test_current_year_in_context(self):
        """ Test if the current year is passed to the template context. """
        response = self.client.get(reverse('home'))
        self.assertIn('current_year', response.context)


class TestContactView(TestCase):
    """ Test cases for the Contact page of the application. """

    def test_contact_page_status_code(self):
        """ Test if the contact page returns a status code of 200. """
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_template_used(self):
        """ Test if the contact page uses the correct template. """
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'main/contact.html')

    def test_contact_page_contains_content(self):
        """ Test if the contact page contains the correct content. """
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'Get in Touch with Medical University')
        self.assertContains(response, 'Tole Bi Street 94, Almaty 050000')
        self.assertContains(response, '+1 (111) 123-4567')
        self.assertContains(response, 'info@medicaluniversity.com')

    def test_google_maps_api_key_in_context(self):
        """Test if the Google Maps API key is passed to the template context."""
        response = self.client.get(reverse('contact'))
        self.assertIn('google_maps_api_key', response.context)
