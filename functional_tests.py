import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class HomepageTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_when_a_search_is_performed(self):
        self.browser.get('http://localhost:8000')
        search_field = self.browser.find_element_by_id('search')
        search_field.send_keys("The Bill")
        search_field.send_keys(Keys.ENTER)
        time.sleep(1)
        current_url: str = self.browser.current_url
        self.assertRegex(current_url, r"^http://\w+:\d+/search.*$")

