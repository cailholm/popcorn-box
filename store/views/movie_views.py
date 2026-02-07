from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from ..models import Movie, MovieTranslation
from ..helpers import TMDBClient
import requests

@login_required
def movie_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = request.user.userprofile
        language = user_profile.language if user_profile.language else 'en'
    except:
        pass
    
    # Récupérer les films avec traductions si disponibles
    movies = Movie.objects.all().order_by('-year')
    
    # Pour chaque film, essayer de récupérer la traduction
    translated_movies = []
    for movie in movies:
        try:
            translation = MovieTranslation.objects.get(movie=movie, language=language)
            movie.title = translation.title
            movie.overview = translation.summary  # Utiliser summary au lieu de overview
        except MovieTranslation.DoesNotExist:
            pass  # Garder les valeurs originales
        translated_movies.append(movie)
    
    return render(request, 'movie_list.html', {
        'movies': translated_movies,
        'title': _('Movie List')
    })

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = request.user.userprofile
        language = user_profile.language if user_profile.language else 'en'
    except:
        pass
    
    # Essayer de récupérer la traduction
    try:
        translation = MovieTranslation.objects.get(movie=movie, language=language)
        movie.title = translation.title
        movie.overview = translation.summary  # Utiliser summary au lieu de overview
    except MovieTranslation.DoesNotExist:
        pass  # Garder les valeurs originales
    
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'title': movie.title
    })

def search_movies_api(request):
    query = request.GET.get('query', '')
    
    if not query:
        return JsonResponse({'results': []})
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = request.user.userprofile
        language = user_profile.language if user_profile.language else 'en'
    except:
        pass
    
    # Utiliser TMDB API pour rechercher des films
    tmdb_client = TMDBClient()
    results = tmdb_client.search_movies(query, language=language)
    
    return JsonResponse({'results': results})