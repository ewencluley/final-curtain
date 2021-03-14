import json
from unittest.mock import patch, MagicMock

import requests_mock
from aiohttp import ClientResponse
from aioresponses import aioresponses
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
        tmdb_mock.search.return_value = [SearchResult(1, 'tv', 'The Bill', 'bill.jpg')]
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(str(response.content), r'.*The Bill.*')


@override_settings(TMDB_API_KEY='mykey')
class TmdbTests(TestCase):

    @requests_mock.Mocker()
    def test_search_with_results(self, requests_mock):
        requests_mock.get(
            'https://api.themoviedb.org/3/search/multi?query=The%20Bill&api_key=mykey&language=en-US&page=1&include_adult=false',
            status_code=200, json={'results': [{'id': 1, 'media_type': 'tv', 'name': 'The Bill', 'poster_path': 'bill.jpg'},
                        {'id': 2, 'media_type': 'movie', 'title': 'Life on Mars', 'poster_path': 'life.jpg'},
                        {'id': 3, 'media_type': 'person', 'name': 'David Bowie', 'profile_path': 'bowie.jpg'}]}
        )

        results = tmdb.search('The Bill')
        self.assertEqual(results, [SearchResult(1, 'tv', 'The Bill', 'bill.jpg'), SearchResult(2, 'movie', 'Life on Mars', 'life.jpg'), SearchResult(3, 'person', 'David Bowie', 'bowie.jpg')])

    @requests_mock.Mocker()
    def test_search_with_no_results(self, requests_mock):
        requests_mock.get(
            'https://api.themoviedb.org/3/search/multi?query=The%20Bill&api_key=mykey&language=en-US&page=1&include_adult=false',
            status_code=200, json={'results': []}
        )

        results = tmdb.search('The Bill')
        self.assertEqual(results, [])

    def test_search_with_no_query(self):
        results = tmdb.search(None)
        self.assertEqual(results, [])

    @requests_mock.Mocker()
    @aioresponses()
    def test_get_cast_tv(self, requests_mock, aio_mock):
        requests_mock.get('https://api.themoviedb.org/3/tv/1/aggregate_credits?api_key=mykey&language=en-US', status_code=200, json=
        {
            'id': 1,
            'cast': [
                {'id': 99, 'roles': [{'character': 'W.P.C. Polly Page'}], 'name': 'Lisa Geoghan',
                 'profile_path': 'lisa.jpg'},
                {'id': 98, 'roles': [{'character': 'D.I. Roy Galloway'}], 'name': 'John Salthouse',
                 'profile_path': 'john.jpg'},
                {'id': 97,
                 'roles': [{'character': 'Dudley'}, {'character': 'Bailiff'}, {'character': 'Mr. Shotten'}],
                 'name': 'Steve Fortune', 'profile_path': 'steve.jpg'}
            ],
            'crew': []
        })

        aio_mock.get('https://api.themoviedb.org/3/person/99?api_key=mykey&language=en-US', status=200, payload={'birthday': '1987-05-08T00:00:00Z','deathday': '2087-05-08T00:00:00Z'})
        aio_mock.get('https://api.themoviedb.org/3/person/98?api_key=mykey&language=en-US', status=200, payload={'birthday': '1949-01-10T00:00:00Z','deathday': '2087-01-01T00:00:00Z'})
        aio_mock.get('https://api.themoviedb.org/3/person/97?api_key=mykey&language=en-US', status=200, payload={'birthday': '1949-01-10T00:00:00Z','deathday': '2087-01-01T00:00:00Z'})
        cast = tmdb.get_cast(1, 'tv')

        self.assertEqual(cast, [
            CastResult(id=99, character='W.P.C. Polly Page', name='Lisa Geoghan', birthday='1987-05-08T00:00:00Z', deathday='2087-05-08T00:00:00Z', has_detail=True),
            CastResult(id=98, character='D.I. Roy Galloway', name='John Salthouse', birthday='1949-01-10T00:00:00Z', deathday='2087-01-01T00:00:00Z', has_detail=True),
            CastResult(97, 'Dudley, Bailiff, Mr. Shotten', 'Steve Fortune', birthday='1949-01-10T00:00:00Z', deathday='2087-01-01T00:00:00Z', has_detail=True),
        ])