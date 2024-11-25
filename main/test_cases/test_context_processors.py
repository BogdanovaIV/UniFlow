from django.test import RequestFactory, TestCase
from datetime import datetime
from main.context_processors import current_year


class ContextProcessorsTests(TestCase):
    """ Tests custom context processors for current year. """
    def setUp(self):
        """ Initializes a request factory for test requests. """
        self.factory = RequestFactory()

    def test_current_year_processor(self):
        """
        Tests that the current_year context processor equal ther year of
        current time
        """
        request = self.factory.get('/')
        context = current_year(request)

        self.assertIn('current_year', context)
        self.assertEqual(context['current_year'], datetime.now().year)
