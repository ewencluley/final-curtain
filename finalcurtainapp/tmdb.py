import requests
from django.conf import settings

from finalcurtainapp.models import SearchResult


def extract_name(item: dict):
    return item.get('title') or item.get('name')


def extract_img(item: dict):
    return item.get('poster_path') or item.get('profile_path')


def search(query):
    if not query:
        return []
    params = {
        'query': query,
        'api_key': settings.TMDB_API_KEY,
        'language': 'en-US',
        'page': 1,
        'include_adult': False
    }
    api_url_base = settings.TMDB_API_BASE_URL
    response = requests.get(f'{api_url_base}/search/multi', params=params)
    return [SearchResult(i['id'], i['media_type'], extract_name(i), extract_img(i)) for i in response.json()['results']]

