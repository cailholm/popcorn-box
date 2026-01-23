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
