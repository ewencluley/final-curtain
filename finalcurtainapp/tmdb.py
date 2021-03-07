import requests
from django.conf import settings

from finalcurtainapp.models import SearchResult, CastResult


def extract_name(item: dict):
    return item.get('title') or item.get('name')


def extract_img(item: dict):
    return item.get('poster_path') or item.get('profile_path')


def extract_character(item: dict):
    if 'roles' in item.keys():
        return ', '.join([r['character'] for r in item.get('roles')])
    return item.get('character')

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
    if response.status_code != 200:
        print(f"response: {response}")
    return [SearchResult(i['id'], i['media_type'], extract_name(i), extract_img(i)) for i in response.json()['results']]


def get_cast(id, media_type):
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'en-US'
    }
    endpoint = 'aggregate_credits' if media_type == 'tv' else 'credits'
    response = requests.get(f'{settings.TMDB_API_BASE_URL}/{media_type}/{id}/{endpoint}', params=params)
    return [CastResult(i['id'], extract_character(i), i['name']) for i in response.json()['cast']]