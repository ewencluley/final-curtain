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
        results = []
        while len(results) == 0:
            time.sleep(0.1)
            results = self.browser.find_element_by_id('results').find_elements_by_tag_name('li')
        for result in results:
            self.assertRegex(result.get_attribute('href'), r'^/cast/\d+$')

