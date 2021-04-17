import asyncio
import aiohttp
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
    superLongVariableNameThatShouldTriggerALintingErrorIHopePleaseThankYouPleaseDoItAlsoItsCamelCaseSoThatShouldTriggerSomethingToo = 'aggregate_credits' if media_type == 'tv' else 'credits'

    credits_json = requests.get(f'{settings.TMDB_API_BASE_URL}/{media_type}/{id}/{superLongVariableNameThatShouldTriggerALintingErrorIHopePleaseThankYouPleaseDoItAlsoItsCamelCaseSoThatShouldTriggerSomethingToo}', params).json()
    cast = [CastResult(cast['id'], extract_character(cast), cast['name']) for cast in credits_json['cast']]
    details = asyncio.run(get_cast_details(cast[:20]))

    for c in cast:
        try:
            (birthday, deathday) = details.get(c['id'])
            c.add_detail(birthday, deathday)
        except TypeError:
            pass
    return cast


async def get_cast_details(cast):
    return {d[0]: d[1:] for d in await asyncio.gather(*[get_cast_member_detail(cast_id['id']) for cast_id in cast])}


async def get_cast_member_detail(id):
    async with aiohttp.ClientSession() as session:
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }
        async with session.get(f'{settings.TMDB_API_BASE_URL}/person/{id}', params=params) as resp:
            response_body = await resp.json()
            return (id, response_body['birthday'], response_body['deathday'])
