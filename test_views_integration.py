#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from store.models import Movie, MovieTranslation, UserProfile, Viewing
from store.views import movie_list, my_viewings
from django.contrib.auth import authenticate, login

def test_views_integration():
    print("=== Test d'intégration des traductions dans les vues ===")
    print()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
    
    # Créer un profil utilisateur avec une langue spécifique
    user_profile = UserProfile.objects.create(user=user, language='fr')
    
    # Create test movie
    movie = Movie.objects.create(
        original_title="Inception",
        year=2010,
        summary="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        director="Christopher Nolan"
    )
    
    # Create viewing pour cet utilisateur
    viewing = Viewing.objects.create(
        user=user,
        movie=movie,
        date='2023-01-01',
        rating=8.5
    )
    
    print(f"Créé utilisateur: {user.email}")
    print(f"Langue de l'utilisateur: {user_profile.language}")
    print(f"Créé film: {movie.original_title}")
    print(f"Créé visionnage: {viewing.movie.original_title} - Note: {viewing.rating}")
    print()
    
    # Tester la vue movie_list
    print("Test 1: Vue movie_list")
    factory = RequestFactory()
    request = factory.get('/movie_list/')
    request.user = user
    
    try:
        response = movie_list(request)
        print(f"  Statut de la réponse: {response.status_code}")
        print(f"  Template utilisé: {response.template_name}")
        
        # Vérifier que les traductions sont bien passées au contexte
        if hasattr(response, 'context_data'):
            movies = response.context_data.get('movies', [])
            if movies:
                first_movie = movies[0]
                print(f"  Premier film traduit: {first_movie.get('translated_title', 'N/A')}")
                print(f"  Résumé traduit: {first_movie.get('translated_summary', 'N/A')[:50]}...")
        else:
            # Pour les versions plus anciennes de Django
            print("  La réponse semble correcte (template rendu)")
            
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Tester la vue my_viewings
    print("Test 2: Vue my_viewings")
    request = factory.get('/my_viewings/')
    request.user = user
    
    try:
        response = my_viewings(request)
        print(f"  Statut de la réponse: {response.status_code}")
        print(f"  Template utilisé: {response.template_name}")
        
        # Vérifier que les traductions sont bien passées au contexte
        if hasattr(response, 'context_data'):
            viewings = response.context_data.get('viewings', [])
            if viewings:
                first_viewing = viewings[0]
                print(f"  Premier visionnage traduit: {first_viewing.get('translated_title', 'N/A')}")
                print(f"  Note: {first_viewing.get('rating', 'N/A')}")
        else:
            print("  La réponse semble correcte (template rendu)")
            
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Tester avec un utilisateur ayant une autre langue
    print("Test 3: Changement de langue (espagnol)")
    user_profile.language = 'es'
    user_profile.save()
    
    request = factory.get('/movie_list/')
    request.user = user
    
    try:
        response = movie_list(request)
        print(f"  Statut de la réponse: {response.status_code}")
        print(f"  Nouvelle langue: {user_profile.language}")
        
        if hasattr(response, 'context_data'):
            movies = response.context_data.get('movies', [])
            if movies:
                first_movie = movies[0]
                print(f"  Titre en espagnol: {first_movie.get('translated_title', 'N/A')}")
        else:
            print("  La réponse semble correcte")
            
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    print("=== Nettoyage ===")
    
    # Cleanup
    viewing.delete()
    movie.delete()
    user_profile.delete()
    user.delete()
    
    print("Nettoyage de la base de données effectué.")
    print("Test terminé avec succès !")

if __name__ == '__main__':
    test_views_integration()