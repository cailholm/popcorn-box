#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Movie, MovieTranslation, UserProfile, Viewing
from store.views import movie_list, my_viewings

def simple_test():
    print("=== Test simple d'intégration ===")
    print()
    
    # Create test user
    user = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpass123')
    user_profile = UserProfile.objects.create(user=user, language='fr')
    
    # Create test movie
    movie = Movie.objects.create(
        original_title="The Dark Knight",
        year=2008,
        summary="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        director="Christopher Nolan"
    )
    
    # Create viewing
    viewing = Viewing.objects.create(
        user=user,
        movie=movie,
        date='2023-01-01',
        rating=9.0
    )
    
    print(f"User: {user.email}")
    print(f"Language: {user_profile.language}")
    print(f"Movie: {movie.original_title}")
    print()
    
    # Test translation logic directly
    print("Testing translation logic:")
    
    # Simulate what movie_list view does
    translation = MovieTranslation.objects.translate(movie, user_profile.language)
    translated_movie = {
        'movie': movie,
        'translated_title': translation.title,
        'translated_summary': translation.summary,
        'year': movie.year,
        'director': movie.director,
        'original_title': movie.original_title,
        'language': user_profile.language
    }
    
    print(f"  Original title: {movie.original_title}")
    print(f"  Translated title: {translated_movie['translated_title']}")
    print(f"  Translated summary: {translated_movie['translated_summary'][:80]}...")
    print()
    
    # Test translation logic for viewings
    print("Testing translation logic for viewings:")
    
    translation = MovieTranslation.objects.translate(viewing.movie, user_profile.language)
    translated_viewing = {
        'viewing': viewing,
        'translated_title': translation.title,
        'translated_summary': translation.summary,
        'year': viewing.movie.year,
        'director': viewing.movie.director,
        'rating': viewing.rating,
        'date': viewing.date
    }
    
    print(f"  Film visionné: {translated_viewing['translated_title']}")
    print(f"  Note: {translated_viewing['rating']}")
    print(f"  Date: {translated_viewing['date']}")
    print()
    
    # Test language change
    print("Testing language change (Spanish):")
    user_profile.language = 'es'
    user_profile.save()
    
    translation = MovieTranslation.objects.translate(movie, user_profile.language)
    print(f"  Title in Spanish: {translation.title}")
    print(f"  Summary in Spanish: {translation.summary[:80]}...")
    print()
    
    # Cleanup
    viewing.delete()
    movie.delete()
    user_profile.delete()
    user.delete()
    
    print("=== Test terminé avec succès ! ===")

if __name__ == '__main__':
    simple_test()