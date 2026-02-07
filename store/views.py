from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.conf import settings
from .models import Movie, Viewing, UserProfile, MovieTranslation
from .helpers import TMDBClient
from pathlib import Path
from dotenv import load_dotenv
import requests
import os

# Load .env file for hCaptcha keys
env_path = Path(__file__).resolve().parent.parent / 'popcorn_box' / '.env'
if env_path.exists():
    load_dotenv(env_path)
import json


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                # Activer la langue de l'utilisateur
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    translation.activate(user_profile.language)
                    request.session['_language'] = user_profile.language
                except UserProfile.DoesNotExist:
                    pass
                return redirect('my_viewings')
            else:
                messages.error(request, _('Invalid email or password.'))
        except User.DoesNotExist:
            messages.error(request, _('Invalid email or password.'))
    return render(request, 'login.html', {'title': _('Sign In')})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        hcaptcha_response = request.POST.get('h-captcha-response')

        # Validation
        if password != password_confirm:
            messages.error(request, _('Passwords do not match.'))
        elif User.objects.filter(username=username).exists():
            messages.error(request, _('Username already exists.'))
        elif User.objects.filter(email=email).exists():
            messages.error(request, _('Email already exists.'))
        elif len(password) < 6:
            messages.error(request, _('Password must be at least 6 characters.'))
        else:
            # Validate hCaptcha manually
            hcaptcha_response = request.POST.get('h-captcha-response')
            if not hcaptcha_response:
                messages.error(request, _('Please complete the CAPTCHA.'))
            else:
                # Use the same validation method as django-hcaptcha package
                from urllib.error import HTTPError
                from urllib.parse import urlencode
                from urllib.request import build_opener, Request, ProxyHandler
                import json
                
                VERIFY_URL = 'https://hcaptcha.com/siteverify'
                TIMEOUT = 10  # seconds
                HCAPTCHA_SECRET_KEY = os.getenv('HCAPTCHA_SECRET_KEY', '0x0000000000000000000000000000000000000000')
                opener = build_opener(ProxyHandler({}))
                post_data = urlencode({
                    'secret': HCAPTCHA_SECRET_KEY,
                    'response': hcaptcha_response,
                }).encode()
                request_captcha = Request(VERIFY_URL, post_data)
                try:
                    response = opener.open(request_captcha, timeout=TIMEOUT)
                    response_data = json.loads(response.read().decode("utf-8"))
                    
                    if not response_data.get('success'):
                        messages.error(request, _('Invalid CAPTCHA. Please try again.'))
                        return render(request, 'signup.html', {
        'title': _('Sign Up'),
        'HCAPTCHA_SITE_KEY': os.getenv('HCAPTCHA_SITE_KEY', '10000000-ffff-ffff-ffff-000000000001')
    })
                except HTTPError:
                    messages.error(request, _('CAPTCHA verification failed. Please try again.'))
                    return render(request, 'signup.html', {'title': _('Sign Up')})
                
                # If we get here, CAPTCHA is valid
                # Créer l'utilisateur (actif immédiatement)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=True  # Compte actif immédiatement
                )
                
                # Créer le profil utilisateur
                user_profile = UserProfile.objects.create(
                    user=user,
                    language='en'
                )

                # Connecter l'utilisateur automatiquement
                login(request, user)
                messages.success(request, _('Account created successfully! Welcome to Popcorn Box!'))
                return redirect('home')

    return render(request, 'signup.html', {
        'title': _('Sign Up'),
        'HCAPTCHA_SITE_KEY': os.getenv('HCAPTCHA_SITE_KEY', '10000000-ffff-ffff-ffff-000000000001')
    })


def movie_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        language = user_profile.language
    except UserProfile.DoesNotExist:
        pass
    
    # Récupérer les films avec leurs traductions
    movies = Movie.objects.all()
    translated_movies = []
    
    for movie in movies:
        # Récupérer ou créer la traduction pour ce film dans la langue de l'utilisateur
        translation = MovieTranslation.objects.translate(movie, language)
        
        translated_movies.append({
            'movie': movie,
            'translated_title': translation.title,
            'translated_summary': translation.summary,
            'year': movie.year,
            'director': movie.director,
            'original_title': movie.original_title,
            'language': language,
            'poster_url': movie.get_poster_url()
        })
    
    return render(request, 'movie_list.html', {'movies': translated_movies, 'language': language, 'title': _('Movie List')})


def logout_view(request):
    # Réinitialiser la langue lors de la déconnexion
    translation.activate('en')
    request.session['_language'] = 'en'
    logout(request)
    return redirect('login')


def my_viewings(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        language = user_profile.language
    except UserProfile.DoesNotExist:
        pass
    
    # Récupérer les visionnages de l'utilisateur connecté avec les traductions (triés par date décroissante)
    viewings = Viewing.objects.filter(user=request.user).select_related('movie').order_by('-date')
    
    # Ajouter les traductions aux visionnages
    translated_viewings = []
    for viewing in viewings:
        translation = MovieTranslation.objects.translate(viewing.movie, language)
        translated_viewings.append({
            'viewing': viewing,
            'movie_id': viewing.movie.id,
            'translated_title': translation.title,
            'translated_summary': translation.summary,
            'year': viewing.movie.year,
            'director': viewing.movie.director,
            'rating': viewing.rating,
            'date': viewing.date,
            'poster_url': viewing.movie.get_poster_url()
        })
    
    return render(request, 'my_viewings.html', {'viewings': translated_viewings, 'language': language, 'title': _('My Viewings')})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer ou créer le profil de l'utilisateur
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in dict(UserProfile.LANGUAGE_CHOICES):
            user_profile.language = language
            user_profile.save()
            # Activer la langue sélectionnée
            translation.activate(language)
            request.session['_language'] = language
            messages.success(request, 'Language updated successfully!')
        else:
            messages.error(request, 'Invalid language selection.')
    
    return render(request, 'profile.html', {'user_profile': user_profile, 'title': _('Profile')})


def add_viewing(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_title = request.POST.get('movie_title')
        date = request.POST.get('date')
        rating = request.POST.get('rating')

        movie = None
        
        # Si un ID de film est fourni, essayer de trouver le film par ID d'abord
        if movie_id:
            # Vérifier si le film existe déjà dans la base de données locale
            movie = Movie.objects.filter(tmdb_id=movie_id).first()
        
        # Si le film n'est pas trouvé par ID, essayer par titre
        if not movie and movie_title:
            movie = Movie.objects.filter(original_title__icontains=movie_title).first()

        # Si le film n'est pas trouvé localement, rechercher dans l'API TMDb
        if not movie and movie_id:
            tmdb_client = TMDBClient()
            try:
                # Récupérer les détails du film à partir de l'ID TMDb
                movie_details = tmdb_client.get_movie_details(movie_id)

                # Récupérer les crédits du film pour obtenir le réalisateur
                credits = tmdb_client.get_movie_credits(movie_id)

                # Extraire le réalisateur
                director = "Unknown"
                for crew_member in credits.get('crew', []):
                    if crew_member.get('job') == 'Director':
                        director = crew_member.get('name')
                        break

                # Télécharger l'affiche du film
                poster_data = tmdb_client.get_poster_base64(movie_details.get('poster_path'))

                # Créer un nouveau film dans la base de données locale
                movie = Movie.objects.create(
                    original_title=movie_details.get('title'),
                    year=int(movie_details.get('release_date', '0000')[:4]) if movie_details.get('release_date') else 0,
                    summary=movie_details.get('overview'),
                    director=director,
                    original_language='en',  # Par défaut anglais, mais pourrait être détecté
                    tmdb_id=movie_id,
                    poster_data=poster_data
                )

                # Créer une traduction pour le film dans la langue par défaut (anglais)
                MovieTranslation.objects.create(
                    movie=movie,
                    language='en',
                    title=movie_details.get('title'),
                    summary=movie_details.get('overview')
                )
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Error fetching movie data: {e}')
                return render(request, 'add_viewing.html', {'title': _('Add Viewing')})
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                return render(request, 'add_viewing.html', {'title': _('Add Viewing')})

        # Créer un nouveau visionnage
        if movie:
            Viewing.objects.create(
                user=request.user,
                movie=movie,
                date=date,
                rating=rating
            )
            messages.success(request, 'Viewing added successfully!')
            return redirect('my_viewings')
        else:
            messages.error(request, 'Movie not found.')

    return render(request, 'add_viewing.html', {'title': _('Add Viewing')})


def movie_detail(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('login')

    movie = get_object_or_404(Movie, id=movie_id)

    # Récupérer la langue de l'utilisateur
    language = 'en'
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        language = user_profile.language
    except UserProfile.DoesNotExist:
        pass

    # Récupérer la traduction
    movie_translation = MovieTranslation.objects.translate(movie, language)

    # Récupérer les visionnages de l'utilisateur pour ce film
    user_viewings = Viewing.objects.filter(user=request.user, movie=movie).order_by('-date')

    context = {
        'title': movie_translation.title,
        'movie': movie,
        'translated_title': movie_translation.title,
        'translated_summary': movie_translation.summary,
        'poster_url': movie.get_poster_url(),
        'viewings': user_viewings,
    }

    return render(request, 'movie_detail.html', context)


def search_movies_api(request):
    """
    API endpoint pour rechercher des films via AJAX
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    query = request.GET.get('query', '').strip()
    page = int(request.GET.get('page', 1))
    
    if len(query) < 2:
        return JsonResponse({'error': _('Please enter at least 2 characters')}, status=400)
    
    try:
        tmdb_client = TMDBClient()
        
        # Get user's language
        language = 'en'  # Default to English
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            language = user_profile.language
        except UserProfile.DoesNotExist:
            pass
        
        # Rechercher dans l'API TMDb avec pagination
        search_results = tmdb_client.search_movie(query, page=page)
        
        movies = []
        for result in search_results.get('results', []):  # Ne plus limiter à 10 résultats
            # Utiliser directement les données de recherche pour éviter un appel API supplémentaire
            # Les données de recherche contiennent déjà les informations nécessaires
            
            # Extract title from search results
            title = result['title']
            
            # Extract overview from search results
            overview = result.get('overview', '')
            
            # Get poster path from search results
            poster_path = result.get('poster_path', None)
            
            movie_data = {
                'id': result['id'],
                'title': title,
                'year': result['release_date'][:4] if result.get('release_date') else 'N/A',
                'overview': overview,
                'poster_path': poster_path
            }
            movies.append(movie_data)
        
        # Ajouter les informations de pagination à la réponse
        response_data = {
            'movies': movies,
            'pagination': {
                'page': page,
                'total_pages': search_results.get('total_pages', 1),
                'total_results': search_results.get('total_results', 0)
            }
        }
        return JsonResponse(response_data, safe=False)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': _('Error fetching movie data: {error}').format(error=str(e))}, status=500)
    except Exception as e:
        return JsonResponse({'error': _('An error occurred: {error}').format(error=str(e))}, status=500)


def home(request):
    """
    Page d'accueil affichant une présentation du site et les films les plus regardés.
    """
    # Récupérer la langue de l'utilisateur (ou langue active si non connecté)
    from django.utils import translation
    language = translation.get_language()
    
    # Récupérer les films les plus regardés au cours des 7 derniers jours
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta
    
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    # Compter les visionnages par film pour les 7 derniers jours (tous les utilisateurs)
    popular_movies_qs = Viewing.objects.filter(
        date__gte=seven_days_ago
    ).values('movie_id', 'movie__original_title', 'movie__poster_data').annotate(
        view_count=Count('id')
    ).order_by('-view_count')[:5]  # Top 5 films

    # Convertir en liste et ajouter les traductions
    popular_movies = []
    for movie in popular_movies_qs:
        movie_data = {
            'movie_id': movie['movie_id'],
            'movie_title': movie['movie__original_title'],
            'poster_url': f"data:image/jpeg;base64,{movie['movie__poster_data']}" if movie['movie__poster_data'] else None,
            'view_count': movie['view_count'],
        }
        try:
            translation_obj = MovieTranslation.objects.get(
                movie_id=movie['movie_id'],
                language=language
            )
            movie_data['translated_title'] = translation_obj.title
        except MovieTranslation.DoesNotExist:
            movie_data['translated_title'] = movie['movie__original_title']
        popular_movies.append(movie_data)
    
    # Préparer les messages de présentation dans la langue de l'utilisateur
    welcome_messages = {
        'en': {
            'welcome': 'Welcome to Popcorn Box!',
            'description': 'Track all the movies you watch and discover your viewing habits.',
            'features': [
                'Add movies you watch with ratings',
                'View your complete viewing history',
                'See statistics about your movie habits',
                'Multilingual support for international films'
            ],
            'popular_title': 'Popular Movies Right Now',
            'no_viewings': 'No movies watched recently.',
            'start_tracking': 'Start tracking your movies now!'
        },
        'fr': {
            'welcome': 'Bienvenue sur Popcorn Box !',
            'description': 'Suivez tous les films que vous regardez et découvrez vos habitudes de visionnage.',
            'features': [
                'Ajoutez des films avec des notes',
                'Consultez votre historique complet',
                'Voyez des statistiques sur vos habitudes',
                'Support multilingue pour les films internationaux'
            ],
            'popular_title': 'Films populaires en ce moment',
            'no_viewings': 'Aucun film regardé récemment.',
            'start_tracking': 'Commencez à suivre vos films maintenant !'
        },
        'es': {
            'welcome': '¡Bienvenido a Popcorn Box!',
            'description': 'Registra todas las películas que ves y descubre tus hábitos de visualización.',
            'features': [
                'Agrega películas con calificaciones',
                'Ve tu historial completo de visualización',
                'Ver estadísticas sobre tus hábitos',
                'Soporte multilingüe para películas internacionales'
            ],
            'popular_title': 'Películas populares ahora',
            'no_viewings': 'No hay películas vistas recientemente.',
            'start_tracking': '¡Empieza a registrar tus películas ahora!'
        },
        'de': {
            'welcome': 'Willkommen bei Popcorn Box!',
            'description': 'Verfolgen Sie alle Filme, die Sie anschauen, und entdecken Sie Ihre Sehgewohnheiten.',
            'features': [
                'Fügen Sie Filme mit Bewertungen hinzu',
                'Sehen Sie Ihre vollständige Verlaufsgeschichte',
                'Sehen Sie Statistiken über Ihre Gewohnheiten',
                'Mehrsprachige Unterstützung für internationale Filme'
            ],
            'popular_title': 'Beliebte Filme jetzt',
            'no_viewings': 'Keine Filme kürzlich angesehen.',
            'start_tracking': 'Fangen Sie jetzt an, Ihre Filme zu verfolgen!'
        }
    }
    
    # Obtenir les messages dans la langue de l'utilisateur
    messages = welcome_messages.get(language, welcome_messages['en'])
    
    context = {
        'title': messages['welcome'],
        'welcome_message': messages['welcome'],
        'description': messages['description'],
        'features': messages['features'],
        'popular_title': messages['popular_title'],
        'no_viewings_message': messages['no_viewings'],
        'start_tracking_message': messages['start_tracking'],
        'popular_movies': popular_movies,
        'language': language
    }
    
    return render(request, 'home.html', context)
