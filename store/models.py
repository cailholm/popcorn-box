from django.db import models
from django.contrib.auth.models import User
import requests
from .helpers import TMDBClient


class Movie(models.Model):
    original_title = models.CharField(max_length=255)
    year = models.IntegerField()
    summary = models.TextField()
    director = models.CharField(max_length=255)
    original_language = models.CharField(max_length=2, default='en')  # Code de langue ISO 639-1
    tmdb_id = models.IntegerField(null=True, blank=True, unique=True)
    poster_data = models.TextField(null=True, blank=True)  # Image en base64

    def __str__(self):
        return f"{self.original_title} ({self.year})"

    def get_poster_url(self):
        """Retourne l'image en data URI pour affichage direct."""
        if self.poster_data:
            return f"data:image/jpeg;base64,{self.poster_data}"
        return None

class MovieTranslationManager(models.Manager):
    def translate(self, movie, language_code):
        """
        Récupère ou crée une traduction pour un film dans une langue spécifique.

        Args:
            movie: Instance du modèle Movie
            language_code: Code de langue (ex: 'fr', 'es', 'de')

        Returns:
            Instance de MovieTranslation
        """
        # D'abord, vérifier si la traduction existe déjà
        try:
            return self.get(movie=movie, language=language_code)
        except MovieTranslation.DoesNotExist:
            pass

        # Si la traduction n'existe pas, essayer de la récupérer depuis TMDb
        tmdb_client = TMDBClient()

        try:
            tmdb_id = movie.tmdb_id

            # Si le film n'a pas de tmdb_id, rechercher dans TMDB
            if not tmdb_id:
                # Stratégie de recherche améliorée pour trouver le bon film dans TMDb
                movie_data = None

                # Stratégie 1: Recherche avec le titre original du film
                data = tmdb_client.search_movie(movie.original_title)

                if data.get('results'):
                    # Trouver le film qui correspond le mieux (par année et titre)
                    for result in data['results']:
                        # Vérifier l'année d'abord
                        year_match = 'release_date' in result and result['release_date'][:4] == str(movie.year)

                        if year_match:
                            movie_data = result
                            break

                    # Si aucun film ne correspond par année, prendre le premier résultat
                    if not movie_data:
                        movie_data = data['results'][0]

                # Stratégie 2: Si nous n'avons pas trouvé de film ou si c'est un film français,
                # essayer aussi avec une recherche en français
                if not movie_data or language_code == 'fr':
                    fr_data = tmdb_client.search_movie(movie.original_title, language='fr-FR')

                    if fr_data.get('results'):
                        for result in fr_data['results']:
                            if 'release_date' in result and result['release_date'][:4] == str(movie.year):
                                movie_data = result
                                break

                        if not movie_data:
                            movie_data = fr_data['results'][0]

                if movie_data:
                    tmdb_id = movie_data["id"]
                    # Stocker l'ID TMDB pour les prochaines requêtes
                    movie.tmdb_id = tmdb_id
                    movie.save(update_fields=['tmdb_id'])

            # Si nous avons un tmdb_id, récupérer les traductions
            if tmdb_id:
                translations_data = tmdb_client.get_movie_translations(tmdb_id)

                # Trouver la traduction pour la langue demandée
                translation_data = None
                for translation in translations_data.get('translations', []):
                    if translation.get('iso_639_1') == language_code:
                        translation_data = translation
                        break

                # Si la traduction est trouvée, créer un nouvel enregistrement
                if translation_data:
                    title = translation_data.get('data', {}).get('title', '')
                    overview = translation_data.get('data', {}).get('overview', movie.summary)

                    # Utiliser le titre original si le titre traduit est vide
                    if not title:
                        title = movie.original_title

                    # Considérer comme fallback uniquement si ni le titre ni le résumé ne sont traduits
                    # (c'est-à-dire si le résumé est le même que l'original)
                    is_fallback = overview == movie.summary

                    return self.create(
                        movie=movie,
                        language=language_code,
                        title=title,
                        summary=overview,
                        is_fallback=is_fallback
                    )

            # Si nous n'avons pas trouvé de film ou de traduction, utiliser le titre original
            return self.create(
                movie=movie,
                language=language_code,
                title=movie.original_title,
                summary=movie.summary,
                is_fallback=True
            )

        except requests.exceptions.RequestException as e:
            # En cas d'erreur avec l'API, créer une entrée avec les données originales
            print(f"Error fetching translation from TMDb: {e}")
            return self.create(
                movie=movie,
                language=language_code,
                title=movie.original_title,
                summary=movie.summary,
                is_fallback=True
            )
        except Exception as e:
            # En cas d'autre erreur, créer une entrée avec les données originales
            print(f"An error occurred: {e}")
            return self.create(
                movie=movie,
                language=language_code,
                title=movie.original_title,
                summary=movie.summary,
                is_fallback=True
            )


class MovieTranslation(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    is_fallback = models.BooleanField(default=False)  # True si aucune traduction n'a été trouvée

    objects = MovieTranslationManager()

    class Meta:
        unique_together = ('movie', 'language')

    def __str__(self):
        return f"{self.movie.original_title} ({self.language})"

class Viewing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return f"{self.user.email} viewed {self.movie.original_title} on {self.date}"

class UserProfile(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return f"{self.user.email}'s profile"


class TMDBApiLog(models.Model):
    url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    http_method = models.CharField(max_length=10, default='GET')
    status_code = models.IntegerField(null=True)
    response = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.http_method} {self.url} - {self.status_code} ({self.timestamp})"
