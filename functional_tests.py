from selenium import webdriver
import unittest


class HomepageTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_homepage_is_rendered(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Final Curtain', self.browser.title)
        self.fail('Finish writing the test!')
