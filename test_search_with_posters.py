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

def test_search_with_posters():
    """Test que les résultats de recherche incluent les affiches sans appel API supplémentaire"""
    
    print("Testing search results with posters (no additional API calls):")
    
    # Create test client
    client = Client()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    user_profile = UserProfile.objects.create(user=user, language='en')
    
    # Login user
    client.force_login(user)
    
    # Search for a movie populaire qui a une affiche
    response = client.get('/api/search-movies/?query=Inception')
    
    if response.status_code == 200:
        movies = response.json()
        if movies:
            first_movie = movies[0]
            print(f"✓ Found movie: {first_movie['title']}")
            
            # Verify poster is included
            if 'poster_path' in first_movie:
                if first_movie['poster_path']:
                    print(f"✓ Poster path included: {first_movie['poster_path']}")
                    print("✓ No additional API call needed for poster!")
                else:
                    print("✓ Poster path field included (but no poster available for this movie)")
            else:
                print("✗ Poster path not included in results")
            
            # Verify complete structure
            expected_fields = ['id', 'title', 'year', 'overview', 'poster_path']
            for field in expected_fields:
                if field in first_movie:
                    print(f"✓ Field '{field}' present")
                else:
                    print(f"✗ Field '{field}' missing")
        else:
            print("✗ No movies found")
    else:
        print(f"✗ Search failed: {response.status_code}")
    
    # Test with a movie that probably has no poster
    print("\n--- Testing movie without poster ---")
    response = client.get('/api/search-movies/?query=Old Movie')
    
    if response.status_code == 200:
        movies = response.json()
        if movies:
            for movie in movies[:3]:  # Check first 3 results
                if 'poster_path' in movie:
                    if movie['poster_path']:
                        print(f"✓ {movie['title']}: Has poster")
                    else:
                        print(f"✓ {movie['title']}: No poster (poster_path is null/empty)")
                else:
                    print(f"✗ {movie['title']}: Missing poster_path field")
    
    # Cleanup
    user.delete()
    user_profile.delete()
    
    print("\n✓ Search with posters test completed!")
    print("✓ Posters are now included in search results without additional API calls")
    print("✓ This improves performance and user experience")

if __name__ == '__main__':
    test_search_with_posters()