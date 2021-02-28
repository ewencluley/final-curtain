from django.http import JsonResponse
from django.shortcuts import render

from finalcurtainapp import tmdb
from finalcurtainapp.models import SearchResult


def home_page(request):
    return render(request, 'home.html')


def search_endpoint(request):
    results = tmdb.search(request.GET.get('q'))
    return JsonResponse(results, safe=False)
