from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _, activate, get_language
from django.utils import translation as translation_utils
from ..models import UserProfile, Movie
from ..helpers import TMDBClient

def home(request):
    if request.user.is_authenticated:
        # Récupérer la langue de l'utilisateur
        language = 'en'  # Langue par défaut
        try:
            user_profile = request.user.userprofile
            language = user_profile.language if user_profile.language else 'en'
        except:
            pass
        
        # La langue devrait déjà être activée par le middleware
        # Mais nous pouvons vérifier et réactiver si nécessaire
        current_lang = translation_utils.get_language()
        if current_lang != language:
            translation_utils.activate(language)
            request.LANGUAGE_CODE = language
        
        # Récupérer un film aléatoire depuis TMDB
        random_movie = None
        try:
            from ..helpers import TMDBClient, TMDBMovie
            
            # Créer un client TMDB
            tmdb_client = TMDBClient()
            
            # Récupérer un film populaire aléatoire depuis TMDB
            tmdb_movie_data = tmdb_client.get_random_popular_movie(language)
            
            if tmdb_movie_data:
                # Sauvegarder le film dans la base de données pour enrichir notre collection
                movie_db, translation_db = tmdb_client.save_tmdb_movie_to_database(tmdb_movie_data, language)
                
                # Créer un wrapper TMDBMovie pour être compatible avec le template
                random_movie = TMDBMovie(tmdb_movie_data, language)
                
        except Exception as e:
            # En cas d'erreur, nous aurons random_movie = None
            print(f"Error getting random movie from TMDB: {e}")
        
        # Récupérer les films populaires (visionnages les plus fréquents)
        popular_movies = []
        try:
            from django.db.models import Count
            # Récupérer les films avec le plus de visionnages
            popular_movies = list(Movie.objects.annotate(
                view_count=Count('viewing')
            ).order_by('-view_count')[:6])
            
            # Ajouter les titres traduits
            for movie in popular_movies:
                try:
                    translation = MovieTranslation.objects.get(movie=movie, language=language)
                    movie.translated_title = translation.title
                except MovieTranslation.DoesNotExist:
                    movie.translated_title = movie.original_title
        except:
            pass
        
        # Messages pour le template (seront traduits par le template)
        context = {
            'title': 'Home',
            'user_language': language,
            'random_movie': random_movie,
            'popular_movies': popular_movies
        }
        
        return render(request, 'home.html', context)
    else:
        # Activer la langue par défaut pour les utilisateurs non connectés
        translation_utils.activate('en')
        request.LANGUAGE_CODE = translation_utils.get_language()
        return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        # Mettre à jour les informations du profil
        language = request.POST.get('language')
        
        try:
            user_profile = request.user.userprofile
            user_profile.language = language
            user_profile.save()
            
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
        except UserProfile.DoesNotExist:
            # Créer un profil si inexistant
            user_profile = UserProfile.objects.create(
                user=request.user,
                language=language
            )
            messages.success(request, _('Profile created successfully!'))
            return redirect('profile')
    
    # Récupérer les informations actuelles du profil
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    
    return render(request, 'profile.html', {
        'title': _('Profile'),
        'user_profile': user_profile
    })