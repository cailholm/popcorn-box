#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from store.models import Movie, MovieTranslation

def test_translation():
    print("Testing MovieTranslation.translate() method...")
    
    # Create test movie
    movie = Movie.objects.create(
        original_title="Inception",
        year=2010,
        summary="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        director="Christopher Nolan"
    )
    
    print(f"Created test movie: {movie.original_title} ({movie.year})")
    
    # Test French translation
    try:
        translation_fr = MovieTranslation.objects.translate(movie, 'fr')
        print(f"French translation created: {translation_fr.title}")
        print(f"French summary: {translation_fr.summary[:100]}...")
    except Exception as e:
        print(f"Error creating French translation: {e}")
    
    # Test Spanish translation
    try:
        translation_es = MovieTranslation.objects.translate(movie, 'es')
        print(f"Spanish translation created: {translation_es.title}")
        print(f"Spanish summary: {translation_es.summary[:100]}...")
    except Exception as e:
        print(f"Error creating Spanish translation: {e}")
    
    # Test retrieval of existing translation
    try:
        existing_translation = MovieTranslation.objects.translate(movie, 'fr')
        print(f"Retrieved existing French translation: {existing_translation.title}")
    except Exception as e:
        print(f"Error retrieving existing translation: {e}")
    
    print("Test completed!")

if __name__ == '__main__':
    test_translation()