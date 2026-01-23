#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from store.views import search_movies_api
from store.models import UserProfile
from django.utils import translation

def test_movie_search():
    """Test de la nouvelle fonctionnalité de recherche de films"""
    
    print("Testing movie search functionality:")
    
    # Create test client
    client = Client()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    user_profile = UserProfile.objects.create(user=user, language='en')
    
    # Login user
    client.force_login(user)
    
    # Test search with different terms
    test_queries = ['Batman', 'Inception', 'The Matrix']
    
    for query in test_queries:
        print(f"\n--- Testing search for: '{query}' ---")
        
        # Faire une requête à l'API de recherche
        response = client.get(f'/api/search-movies/?query={query}')
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} movies:")
            for i, movie in enumerate(data[:3]):  # Afficher les 3 premiers résultats
                print(f"  {i+1}. {movie['title']} ({movie['year']})")
        else:
            print(f"Error: {response.content}")
    
    # Tester avec une requête trop courte
    print(f"\n--- Testing short query ---")
    response = client.get('/api/search-movies/?query=a')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content}")
    
    # Cleanup
    user.delete()
    user_profile.delete()
    
    print("\n✓ Movie search functionality test completed!")

if __name__ == '__main__':
    test_movie_search()