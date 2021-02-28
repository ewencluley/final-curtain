import json
from unittest.mock import patch

from django.test import TestCase, override_settings

from finalcurtainapp import tmdb
from finalcurtainapp.models import SearchResult


class HomepageTest(TestCase):

    def test_homepage_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


@patch("finalcurtainapp.views.tmdb", autospec=True)
class SearchTest(TestCase):

    def test_search_returns_expected_json(self, tmdb_mock):
        tmdb_mock.search.return_value = [SearchResult(1, 'tv')]
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [{'id': 1, 'media_type': 'tv'}])


@patch('finalcurtainapp.tmdb.requests', autospec=True)
@override_settings(TMDB_API_KEY='mykey')
class TmdbTests(TestCase):

    def test_search_with_results(self, requests_mock):
        requests_mock.get.return_value.status_code = 200
        requests_mock.get.return_value.json.return_value = {'results': [{'id': 1, 'media_type': 'tv'}]}

        results = tmdb.search('The Bill')
        requests_mock.get.assert_called_with(
            'https://api.themoviedb.org/3/search/multi',
            params={'query': 'The Bill', 'api_key': 'mykey', 'language': 'en-US', 'page': 1, 'include_adult': False}
        )
        self.assertEqual(results, [SearchResult(1, 'tv')])

    def test_search_with_no_results(self, requests_mock):
        requests_mock.get.return_value.status_code = 200
        requests_mock.get.return_value.json.return_value = {'results': []}

        results = tmdb.search('The Bill')
        requests_mock.get.assert_called_with(
            'https://api.themoviedb.org/3/search/multi',
            params={'query': 'The Bill', 'api_key': 'mykey', 'language': 'en-US', 'page': 1, 'include_adult': False}
        )
        self.assertEqual(results, [])
