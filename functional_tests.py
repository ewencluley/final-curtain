import asyncio
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


async def get_results(browser, results_container_id, element_tag):
    results = []
    while len(results) == 0:
        await asyncio.sleep(0.1)
        results = browser.find_element_by_id(results_container_id).find_elements_by_tag_name(element_tag)
    return results


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

        results = asyncio.run(asyncio.wait_for(get_results(self.browser, 'results', 'a'), timeout=10))
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertRegex(result.get_attribute('href'), r'\d+/cast$')

    def test_when_a_search_result_is_clicked(self):
        self.browser.get('http://localhost:8000/tv/2072/cast')

        results = asyncio.run(asyncio.wait_for(get_results(self.browser, 'results', 'li'), timeout=10))
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual('list-group-item', result.get_attribute('class'))