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

def test_grand_chemin():
    print("=== Test spécifique pour 'Le Grand Chemin' ===")
    print()
    
    # Créer le film "Le Grand Chemin" (qui est déjà en français dans la base)
    movie = Movie.objects.create(
        original_title="Le Grand Chemin",
        year=1987,
        summary="Louis, un jeune garçon de Paris, est envoyé passer ses vacances à la campagne chez ses grands-parents. Il découvre un monde nouveau et se lie d'amitié avec un vieux monsieur solitaire.",
        director="Jean-Loup Hubert"
    )
    
    print(f"Film créé: {movie.original_title} ({movie.year})")
    print(f"Directeur: {movie.director}")
    print()
    
    # Test French translation (devrait utiliser le titre existant)
    print("Test 1: Traduction en français")
    try:
        translation_fr = MovieTranslation.objects.translate(movie, 'fr')
        print(f"  Titre français: {translation_fr.title}")
        print(f"  Résumé français: {translation_fr.summary[:100]}...")
        print(f"  Résultat: {'OK' if translation_fr.title == 'Le Grand Chemin' else 'Échec - titre incorrect'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Tester la traduction en anglais (devrait obtenir la traduction depuis TMDb)
    print("Test 2: Traduction en anglais")
    try:
        translation_en = MovieTranslation.objects.translate(movie, 'en')
        print(f"  Titre anglais: {translation_en.title}")
        print(f"  Résumé anglais: {translation_en.summary[:100]}...")
        print(f"  Résultat: {'OK' if translation_en.title != 'Le Grand Chemin' else 'Échec - titre non traduit'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Test Spanish translation
    print("Test 3: Traduction en espagnol")
    try:
        translation_es = MovieTranslation.objects.translate(movie, 'es')
        print(f"  Titre espagnol: {translation_es.title}")
        print(f"  Résumé espagnol: {translation_es.summary[:100]}...")
        print(f"  Résultat: {'OK' if translation_es.title != 'Le Grand Chemin' else 'Échec - titre non traduit'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Tester avec un film qui a un titre anglais mais devrait avoir une traduction française
    print("Test 4: Film avec titre anglais mais traduction française disponible")
    movie2 = Movie.objects.create(
        original_title="The Grand Highway",  # Titre anglais
        year=1987,
        summary="A story about a young boy discovering the countryside.",
        director="Jean-Loup Hubert"
    )
    
    try:
        translation_fr2 = MovieTranslation.objects.translate(movie2, 'fr')
        print(f"  Titre original: {movie2.original_title}")
        print(f"  Titre français: {translation_fr2.title}")
        print(f"  Résultat: {'OK' if translation_fr2.title == 'Le Grand Chemin' else 'Échec - devrait être Le Grand Chemin'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Cleanup
    movie.delete()
    movie2.delete()
    
    print("=== Test terminé ===")
    print("Le test montre comment la méthode améliorée gère les films avec des titres")
    print("déjà dans la langue cible et les films qui nécessitent une traduction.")

if __name__ == '__main__':
    test_grand_chemin()