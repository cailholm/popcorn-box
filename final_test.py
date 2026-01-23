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

def final_test():
    print("=== Final Test of MovieTranslation.translate() ===")
    print()
    
    # Test 1: Popular movie with available translations
    print("Test 1: Popular movie (The Matrix)")
    matrix = Movie.objects.create(
        original_title="The Matrix",
        year=1999,
        summary="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        director="Lana Wachowski"
    )
    
    # Test multiple languages
    languages = ['fr', 'es', 'de']
    for lang in languages:
        try:
            translation = MovieTranslation.objects.translate(matrix, lang)
            print(f"  {lang.upper()}: {translation.title}")
            print(f"    Summary: {translation.summary[:80]}...")
        except Exception as e:
            print(f"  {lang.upper()}: Error - {e}")
    
    print()
    
    # Test 2: Verify translations are properly stored in database
    print("Test 2: Database storage verification")
    stored_translations = MovieTranslation.objects.filter(movie=matrix)
    print(f"  Number of stored translations: {stored_translations.count()}")
    for trans in stored_translations:
        print(f"    {trans.language}: {trans.title}")
    
    print()
    
    # Test 3: Verify retrieval of existing translation works
    print("Test 3: Retrieval of existing translations")
    existing_fr = MovieTranslation.objects.translate(matrix, 'fr')
    print(f"  Retrieved French translation: {existing_fr.title}")
    print(f"  Translation ID: {existing_fr.id}")
    
    print()
    
    # Test 4: Movie with title that might not have translation
    print("Test 4: Less known movie (test with generic title)")
    test_movie = Movie.objects.create(
        original_title="Test Movie",
        year=2020,
        summary="This is a test movie for translation functionality.",
        director="Test Director"
    )
    
    try:
        test_translation = MovieTranslation.objects.translate(test_movie, 'fr')
        print(f"  Result: {test_translation.title}")
        print(f"  Summary: {test_translation.summary[:50]}...")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()
    print("=== Test terminé ===")
    
    # Cleanup
    matrix.delete()
    test_movie.delete()
    print("Nettoyage de la base de données effectué.")

if __name__ == '__main__':
    final_test()