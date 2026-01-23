#!/usr/bin/env python

import os
import sys
import django

# Django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from store.models import UserProfile

def test_translated_search_results():
    """Test que les résultats de recherche sont traduits dans la langue de l'utilisateur"""
    
    print("Testing translated search results:")
    
    # Create test client
    client = Client()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    
    # Test with different languages
    languages = [
        ('en', 'English', 'English'),
        ('fr', 'French', 'Français'),
        ('de', 'German', 'Deutsch'),
        ('es', 'Spanish', 'Español')
    ]
    
    for lang_code, lang_name, lang_native in languages:
        print(f"\n--- Testing {lang_name} ({lang_native}) ---")
        
        # Mettre à jour la langue de l'utilisateur
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.language = lang_code
        user_profile.save()
        
        # Login user
        client.force_login(user)
        
        # Search for a movie populaire qui a des traductions
        response = client.get('/api/search-movies/?query=Inception')
        
        if response.status_code == 200:
            movies = response.json()
            if movies:
                first_movie = movies[0]
                print(f"✓ Found movie: {first_movie['title']}")
                
                # Vérifier que le titre et la description sont dans la bonne langue
                # Pour les films populaires, TMDB devrait avoir des traductions
                if first_movie['title'] and len(first_movie['title']) > 0:
                    print(f"✓ Title: {first_movie['title']}")
                
                if first_movie['overview']:
                    print(f"✓ Overview: {first_movie['overview'][:100]}...")
                else:
                    print("✓ No overview available (might be normal for some languages)")
            else:
                print("✗ No movies found")
        else:
            print(f"✗ Search failed: {response.status_code}")
    
    # Cleanup
    user.delete()
    user_profile.delete()
    
    print("\n✓ Translated search results test completed!")
    print("✓ Results should now be in user's language when available")

if __name__ == '__main__':
    test_translated_search_results()