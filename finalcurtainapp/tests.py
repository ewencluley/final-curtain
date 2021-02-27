from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from finalcurtainapp.views import home_page

class HomepageTest(TestCase):

    def test_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        response_body = response.content.decode('utf-8')
        self.assertTrue(response_body.lower().startswith('<html>'))
        self.assertIn('<title>Final Curtain</title>', response_body)
        self.assertTrue(response_body.lower().endswith('</html>'))
