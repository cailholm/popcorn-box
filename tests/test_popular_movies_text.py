#!/usr/bin/env python

import os
import sys
import django

# Ajouter le chemin du projet au path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import Client

def test_popular_movies_text():
    """Test des nouveaux textes pour les films populaires"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST: NOUVEAUX TEXTES FILMS POPULAIRES")
    print("=" * 60)
    
    # Test 1: Anglais
    print("\n1. Test en anglais")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9')
    content = response.content.decode('utf-8')
    
    if 'Popular Movies Right Now' in content:
        print("✓ Texte anglais correct: 'Popular Movies Right Now'")
    else:
        print("✗ Texte anglais incorrect")
        # Chercher ce qui est présent
        if 'Most Watched Movies' in content:
            print("  Ancien texte encore présent: 'Most Watched Movies'")
        if 'No movies watched recently' in content:
            print("✓ Message 'No movies watched recently' présent")
    
    # Test 2: Français
    print("\n2. Test en français")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
    content = response.content.decode('utf-8')
    
    if 'Films populaires en ce moment' in content:
        print("✓ Texte français correct: 'Films populaires en ce moment'")
    else:
        print("✗ Texte français incorrect")
        if 'Films les plus regardés' in content:
            print("  Ancien texte encore présent: 'Films les plus regardés'")
        if 'Aucun film regardé récemment' in content:
            print("✓ Message 'Aucun film regardé récemment' présent")
    
    # Test 3: Espagnol
    print("\n3. Test en espagnol")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='es-ES,es;q=0.9')
    content = response.content.decode('utf-8')
    
    if 'Películas populares ahora' in content:
        print("✓ Texte espagnol correct: 'Películas populares ahora'")
    else:
        print("✗ Texte espagnol incorrect")
        if 'Películas más vistas' in content:
            print("  Ancien texte encore présent: 'Películas más vistas'")
        if 'No hay películas vistas recientemente' in content:
            print("✓ Message 'No hay películas vistas recientemente' présent")
    
    # Test 4: Allemand
    print("\n4. Test en allemand")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='de-DE,de;q=0.9')
    content = response.content.decode('utf-8')
    
    if 'Beliebte Filme jetzt' in content:
        print("✓ Texte allemand correct: 'Beliebte Filme jetzt'")
    else:
        print("✗ Texte allemand incorrect")
        if 'Meistgesehene Filme' in content:
            print("  Ancien texte encore présent: 'Meistgesehene Filme'")
        if 'Keine Filme kürzlich angesehen' in content:
            print("✓ Message 'Keine Filme kürzlich angesehen' présent")
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)
    
    print("\nSi les tests échouent, vérifiez que:")
    print("- Les modifications ont été sauvegardées")
    print("- Le serveur a été redémarré (si en mode développement)")
    print("- Les traductions sont correctement définies dans le code")

if __name__ == '__main__':
    test_popular_movies_text()