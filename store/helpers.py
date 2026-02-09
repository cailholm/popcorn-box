import base64
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'popcorn_box', '.env'))

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '0d52b79b3e5cf36801f31ccfda872d54')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/'


class TMDBClient:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL

    def _make_request(self, url):
        """
        Fait un appel HTTP GET et log dans TMDBApiLog.

        Args:
            url: URL complète de l'API TMDB

        Returns:
            dict: Réponse JSON de l'API

        Raises:
            requests.exceptions.RequestException: En cas d'erreur HTTP
        """
        # Import local pour éviter les imports circulaires
        from .models import TMDBApiLog

        response = requests.get(url)

        # Logger l'appel API
        TMDBApiLog.objects.create(
            url=url,
            http_method='GET',
            status_code=response.status_code,
            response=response.text[:10000] if response.text else None  # Limiter la taille
        )

        response.raise_for_status()
        return response.json()

    def search_movie(self, query, language=None, page=1):
        """
        Recherche de films par titre.

        Args:
            query: Terme de recherche
            language: Code de langue optionnel (ex: 'fr-FR')
            page: Numéro de page pour la pagination (par défaut: 1)

        Returns:
            dict: Résultats de recherche
        """
        url = f'{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}'
        if language:
            url += f'&language={language}'
        return self._make_request(url)

    def get_movie_details(self, movie_id, language=None):
        """
        Récupère les détails d'un film.

        Args:
            movie_id: ID TMDB du film
            language: Code de langue optionnel (ex: 'fr-FR')

        Returns:
            dict: Détails du film
        """
        url = f'{self.base_url}/movie/{movie_id}?api_key={self.api_key}'
        if language:
            url += f'&language={language}'
        return self._make_request(url)

    def get_movie_translations(self, movie_id):
        """
        Récupère les traductions d'un film.

        Args:
            movie_id: ID TMDB du film

        Returns:
            dict: Traductions du film
        """
        url = f'{self.base_url}/movie/{movie_id}/translations?api_key={self.api_key}'
        return self._make_request(url)

    def get_movie_credits(self, movie_id):
        """
        Récupère les crédits d'un film.

        Args:
            movie_id: ID TMDB du film

        Returns:
            dict: Crédits du film (cast et crew)
        """
        url = f'{self.base_url}/movie/{movie_id}/credits?api_key={self.api_key}'
        return self._make_request(url)

    def get_poster_base64(self, poster_path, size='w185'):
        """
        Télécharge l'affiche d'un film et la retourne en base64.

        Args:
            poster_path: Chemin de l'affiche retourné par TMDB (ex: '/abc123.jpg')
            size: Taille de l'image (w92, w154, w185, w342, w500, w780, original)

        Returns:
            str: Image encodée en base64, ou None si erreur
        """
        if not poster_path:
            return None

        from .models import TMDBApiLog

        url = f'{TMDB_IMAGE_BASE_URL}{size}{poster_path}'
        try:
            response = requests.get(url)

            # Logger l'appel API
            TMDBApiLog.objects.create(
                url=url,
                http_method='GET',
                status_code=response.status_code,
                response=f'[Image binary data - {len(response.content)} bytes]'
            )

            response.raise_for_status()
            return base64.b64encode(response.content).decode('utf-8')
        except requests.exceptions.RequestException:
            return None

    def get_popular_movies(self, language=None, page=1):
        """
        Récupère une liste de films populaires depuis TMDB.

        Args:
            language: Code de langue optionnel (ex: 'fr-FR')
            page: Numéro de page pour la pagination (par défaut: 1)

        Returns:
            dict: Liste de films populaires
        """
        url = f'{self.base_url}/discover/movie?api_key={self.api_key}&sort_by=popularity.desc&page={page}'
        if language:
            url += f'&language={language}'
        return self._make_request(url)

    def get_random_popular_movie(self, language=None):
        """
        Récupère un film populaire aléatoire depuis TMDB.

        Args:
            language: Code de langue optionnel (ex: 'fr-FR')

        Returns:
            dict: Un film populaire aléatoire
        """
        # Récupérer la première page de films populaires
        popular_movies = self.get_popular_movies(language, page=1)
        
        if popular_movies and popular_movies.get('results'):
            import random
            return random.choice(popular_movies['results'])
        
        return None

    def save_tmdb_movie_to_database(self, tmdb_movie_data, language='en'):
        """
        Sauvegarde un film TMDB dans la base de données locale.

        Args:
            tmdb_movie_data: Données du film depuis TMDB
            language: Code de langue pour les traductions (ex: 'fr', 'de', 'es')

        Returns:
            tuple: (movie_instance, translation_instance) ou (None, None) en cas d'erreur
        """
        try:
            from .models import Movie, MovieTranslation
            
            # Extraire les données nécessaires
            tmdb_id = tmdb_movie_data.get('id')
            original_title = tmdb_movie_data.get('original_title', tmdb_movie_data.get('title', 'Unknown Title'))
            
            # Extraire l'année depuis la date de sortie
            release_date = tmdb_movie_data.get('release_date')
            year = int(release_date[:4]) if release_date and len(release_date) >= 4 else None
            
            # Si nous n'avons pas d'année, utiliser l'année actuelle
            import datetime
            if not year:
                year = datetime.datetime.now().year
            
            # Extraire le résumé
            summary = tmdb_movie_data.get('overview', '')
            
            # Extraire le réalisateur (si disponible dans les crédits)
            director = 'Unknown'
            
            # Récupérer l'affiche en base64
            poster_path = tmdb_movie_data.get('poster_path')
            poster_data = None
            if poster_path:
                poster_data = self.get_poster_base64(poster_path, 'w342')
            
            # Vérifier si le film existe déjà dans la base de données
            try:
                movie = Movie.objects.get(tmdb_id=tmdb_id)
                # Mettre à jour les informations si nécessaire
                movie.original_title = original_title
                movie.year = year
                movie.summary = summary
                if poster_data:
                    movie.poster_data = poster_data
                movie.save()
                print(f"Movie updated in database: {original_title} ({year})")
            except Movie.DoesNotExist:
                # Créer un nouveau film
                movie = Movie.objects.create(
                    original_title=original_title,
                    year=year,
                    summary=summary,
                    director=director,
                    original_language=language,
                    tmdb_id=tmdb_id,
                    poster_data=poster_data
                )
                print(f"New movie saved to database: {original_title} ({year})")
            
            # Sauvegarder la traduction si la langue n'est pas l'anglais
            translation = None
            if language != 'en':
                try:
                    translation = MovieTranslation.objects.get(movie=movie, language=language)
                    # Mettre à jour la traduction existante
                    translation.title = tmdb_movie_data.get('title', original_title)
                    translation.summary = tmdb_movie_data.get('overview', summary)
                    translation.save()
                    print(f"Translation updated: {language} for {original_title}")
                except MovieTranslation.DoesNotExist:
                    # Créer une nouvelle traduction
                    translation = MovieTranslation.objects.create(
                        movie=movie,
                        language=language,
                        title=tmdb_movie_data.get('title', original_title),
                        summary=tmdb_movie_data.get('overview', summary),
                        is_fallback=False
                    )
                    print(f"New translation saved: {language} for {original_title}")
            
            return movie, translation
            
        except Exception as e:
            print(f"Error saving TMDB movie to database: {e}")
            import traceback
            traceback.print_exc()
            return None, None


class TMDBMovie:
    """
    Classe wrapper pour les films TMDB afin de les rendre compatibles avec les templates.
    """
    
    def __init__(self, tmdb_data, language='en'):
        self.tmdb_data = tmdb_data
        self.language = language
        
    @property
    def id(self):
        return self.tmdb_data.get('id')
    
    @property
    def translated_title(self):
        return self.tmdb_data.get('title', self.tmdb_data.get('original_title', 'Unknown Title'))
    
    @property
    def year(self):
        release_date = self.tmdb_data.get('release_date')
        if release_date and len(release_date) >= 4:
            return release_date[:4]
        return None
    
    @property
    def overview(self):
        return self.tmdb_data.get('overview', '')
    
    @property
    def poster_path(self):
        return self.tmdb_data.get('poster_path')
    
    def get_poster_url(self):
        if self.poster_path:
            return f'{TMDB_IMAGE_BASE_URL}w342{self.poster_path}'
        return None
