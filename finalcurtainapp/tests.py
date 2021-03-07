import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings

from finalcurtainapp import tmdb
from finalcurtainapp.models import SearchResult, CastResult


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
        requests_mock.get.return_value.json.return_value = {
            'results': [{'id': 1, 'media_type': 'tv', 'name': 'The Bill', 'poster_path': 'bill.jpg'},
                        {'id': 2, 'media_type': 'movie', 'title': 'Life on Mars', 'poster_path': 'life.jpg'},
                        {'id': 3, 'media_type': 'person', 'name': 'David Bowie', 'profile_path': 'bowie.jpg'}]}

        results = tmdb.search('The Bill')
        requests_mock.get.assert_called_with(
            'https://api.themoviedb.org/3/search/multi',
            params={'query': 'The Bill', 'api_key': 'mykey', 'language': 'en-US', 'page': 1, 'include_adult': False}
        )
        self.assertEqual(results, [SearchResult(1, 'tv', 'The Bill', 'bill.jpg'), SearchResult(2, 'movie', 'Life on Mars', 'life.jpg'), SearchResult(3, 'person', 'David Bowie', 'bowie.jpg')])

    def test_search_with_no_results(self, requests_mock):
        requests_mock.get.return_value.status_code = 200
        requests_mock.get.return_value.json.return_value = {'results': []}

        results = tmdb.search('The Bill')
        requests_mock.get.assert_called_with(
            'https://api.themoviedb.org/3/search/multi',
            params={'query': 'The Bill', 'api_key': 'mykey', 'language': 'en-US', 'page': 1, 'include_adult': False}
        )
        self.assertEqual(results, [])

    def test_search_with_no_query(self, requests_mock):
        results = tmdb.search(None)
        self.assertEqual(results, [])

    def test_get_cast_tv(self, requests_mock):
        def get_mock_response(url: str, params):
            if url.endswith('/tv/1/aggregate_credits'):
                resp = MagicMock()
                resp.status_code = 200
                resp.json.return_value = {
                    'id': 1,
                    'cast': [
                        {'id': 99, 'roles': [{'character': 'W.P.C. Polly Page'}], 'name': 'Lisa Geoghan', 'profile_path': 'lisa.jpg'},
                        {'id': 98, 'roles': [{'character': 'D.I. Roy Galloway'}], 'name': 'John Salthouse', 'profile_path': 'john.jpg'},
                        {'id': 97, 'roles': [{'character': 'Dudley'}, {'character': 'Bailiff'}, {'character': 'Mr. Shotten'}], 'name': 'Steve Fortune', 'profile_path': 'steve.jpg'}
                    ],
                    'crew': []
                }
                return resp
            else:
                raise Exception("get called with unexpected url")

        requests_mock.get = get_mock_response

        cast = tmdb.get_cast(1, 'tv')

        self.assertEqual(cast, [
            CastResult(99, 'W.P.C. Polly Page', 'Lisa Geoghan'),
            CastResult(98, 'D.I. Roy Galloway', 'John Salthouse'),
            CastResult(97, 'Dudley, Bailiff, Mr. Shotten', 'Steve Fortune'),
        ])

    def test_get_cast_movie(self, requests_mock):
        def get_mock_response(url: str, params):
            if url.endswith('/movie/1/credits'):
                resp = MagicMock()
                resp.status_code = 200
                resp.json.return_value = {
                    'id': 1,
                    'cast': [
                        {'id': 99, 'character': 'W.P.C. Polly Page', 'name': 'Lisa Geoghan', 'profile_path': 'lisa.jpg'},
                        {'id': 98, 'character': 'D.I. Roy Galloway', 'name': 'John Salthouse', 'profile_path': 'john.jpg'},
                        {'id': 97, 'character': 'Dudley', 'name': 'Steve Fortune', 'profile_path': 'steve.jpg'}
                    ],
                    'crew': []
                }
                return resp
            else:
                raise Exception("get called with unexpected url")

        requests_mock.get = get_mock_response

        cast = tmdb.get_cast(1, 'movie')

        self.assertEqual(cast, [
            CastResult(99, 'W.P.C. Polly Page', 'Lisa Geoghan'),
            CastResult(98, 'D.I. Roy Galloway', 'John Salthouse'),
            CastResult(97, 'Dudley', 'Steve Fortune'),
        ])