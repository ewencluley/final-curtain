import requests
from django.conf import settings

from finalcurtainapp.models import SearchResult


def search(query):
    params = {
        'query': query,
        'api_key': settings.TMDB_API_KEY,
        'language': 'en-US',
        'page': 1,
        'include_adult': False
    }
    api_url_base = settings.TMDB_API_BASE_URL
    response = requests.get(f'{api_url_base}/search/multi', params=params)
    return [SearchResult(i['id'], i['media_type']) for i in response.json()['results']]
