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

def test_original_title_rule():
    print("=== Test de la règle du titre original ===")
    print()
    
    # Test 1: Film avec titre original français
    print("Test 1: Film avec titre original français ('Le Grand Chemin')")
    movie1 = Movie.objects.create(
        original_title="Le Grand Chemin",
        year=1987,
        summary="Un jeune garçon découvre la campagne française.",
        director="Jean-Loup Hubert",
        original_language='fr'
    )
    
    print(f"  Titre original: {movie1.original_title}")
    print(f"  Langue originale: {movie1.original_language}")
    
    # Traduction en français (devrait utiliser le titre original)
    translation_fr = MovieTranslation.objects.translate(movie1, 'fr')
    print(f"  Traduction FR: {translation_fr.title}")
    print(f"  Résultat: {'OK' if translation_fr.title == 'Le Grand Chemin' else 'Échec'}")
    
    # Traduction en anglais (devrait obtenir la traduction depuis TMDb)
    translation_en = MovieTranslation.objects.translate(movie1, 'en')
    print(f"  Traduction EN: {translation_en.title}")
    print(f"  Résultat: {'OK' if translation_en.title != 'Le Grand Chemin' else 'Échec - devrait être traduit'}")
    
    # Traduction en espagnol (devrait utiliser le titre original si pas de traduction)
    translation_es = MovieTranslation.objects.translate(movie1, 'es')
    print(f"  Traduction ES: {translation_es.title}")
    print(f"  Résultat: {'OK' if translation_es.title == 'Le Grand Chemin' else 'Échec - devrait utiliser le titre original'}")
    
    print()
    
    # Test 2: Film avec titre original anglais
    print("Test 2: Film avec titre original anglais ('The Grand Highway')")
    movie2 = Movie.objects.create(
        original_title="The Grand Highway",
        year=1987,
        summary="A story about a young boy discovering the countryside.",
        director="Jean-Loup Hubert",
        original_language='en'
    )
    
    print(f"  Titre original: {movie2.original_title}")
    print(f"  Langue originale: {movie2.original_language}")
    
    # Traduction en français (devrait obtenir la traduction depuis TMDb)
    translation_fr2 = MovieTranslation.objects.translate(movie2, 'fr')
    print(f"  Traduction FR: {translation_fr2.title}")
    print(f"  Résultat: {'OK' if translation_fr2.title == 'Le Grand Chemin' else 'Échec - devrait être Le Grand Chemin'}")
    
    # Traduction en anglais (devrait utiliser le titre original)
    translation_en2 = MovieTranslation.objects.translate(movie2, 'en')
    print(f"  Traduction EN: {translation_en2.title}")
    print(f"  Résultat: {'OK' if translation_en2.title == 'The Grand Highway' else 'Échec'}")
    
    print()
    
    # Test 3: Vérification que les traductions existent bien en base
    print("Test 3: Vérification du stockage des traductions")
    all_translations = MovieTranslation.objects.filter(movie__in=[movie1, movie2])
    print(f"  Nombre total de traductions: {all_translations.count()}")
    for trans in all_translations:
        print(f"    Film: {trans.movie.original_title}, Langue: {trans.language}, Titre: {trans.title}")
    
    print()
    
    # Cleanup
    movie1.delete()
    movie2.delete()
    
    print("=== Test terminé ===")
    print("La règle est maintenant implémentée:")
    print("- Les films ont un titre original (original_title) et une langue originale")
    print("- Les traductions utilisent le titre original si aucune traduction n'est disponible")
    print("- Les traductions sont stockées dans MovieTranslation avec le bon titre")

if __name__ == '__main__':
    test_original_title_rule()