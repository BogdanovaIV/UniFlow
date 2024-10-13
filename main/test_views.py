from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):

    def test_home_page_status_code(self):
        """Test if the home page returns a 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test if the home page uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_home_page_contains_correct_html(self):
        """Test if the home page contains specific text."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Medical University')
