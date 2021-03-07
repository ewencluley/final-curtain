from django.http import JsonResponse
from django.shortcuts import render

from finalcurtainapp import tmdb
from finalcurtainapp.models import SearchResult


def home_page(request):
    return render(request, 'home.html')


def search_page(request):
    results = tmdb.search(request.GET.get('q'))
    return render(request=request, template_name='search.html', context={'results': results})
