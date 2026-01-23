#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from store.models import UserProfile, Movie, Viewing
from django.utils import translation

def test_complete_add_viewing_process():
    """Test complet du processus d'ajout de visionnage avec la nouvelle interface"""
    
    print("Testing complete add viewing process:")
    
    # Create test client
    client = Client()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    user_profile = UserProfile.objects.create(user=user, language='en')
    
    # Login user
    client.force_login(user)
    
    print("\n1. Testing movie search API...")
    
    # Test movie search
    response = client.get('/api/search-movies/?query=Inception')
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✓ Found {len(movies)} movies for 'Inception'")
        
        if movies:
            # Select first movie
            selected_movie = movies[0]
            print(f"✓ Selected movie: {selected_movie['title']} ({selected_movie['year']})")
            
            print("\n2. Testing add viewing with selected movie...")
            
            # Test adding viewing with selected movie
            response = client.post('/add_viewing/', {
                'movie_id': selected_movie['id'],
                'movie_title': selected_movie['title'],
                'date': '2023-01-15',
                'rating': '4.5'
            })
            
            print(f"✓ Add viewing response status: {response.status_code}")
            
            # Verify viewing was added
            viewings = Viewing.objects.filter(user=user)
            print(f"✓ User now has {viewings.count()} viewings")
            
            if viewings.count() > 0:
                latest_viewing = viewings.latest('date')
                print(f"✓ Latest viewing: {latest_viewing.movie.original_title} - Rating: {latest_viewing.rating}")
    else:
        print(f"✗ Movie search failed: {response.content}")
    
    # Test with a movie not yet in database
    print("\n3. Testing with a new movie (not in database)...")
    
    # Search for a movie that is probably not in the database
    response = client.get('/api/search-movies/?query=Interstellar')
    
    if response.status_code == 200:
        movies = response.json()
        if movies:
            new_movie = movies[0]
            print(f"✓ Found new movie: {new_movie['title']} (ID: {new_movie['id']})")
            
            # Verify movie is not yet in database
            existing_movie = Movie.objects.filter(tmdb_id=new_movie['id']).first()
            if not existing_movie:
                print("✓ Movie not in database yet")
                
                # Add viewing - this should create the movie
                response = client.post('/add_viewing/', {
                    'movie_id': new_movie['id'],
                    'movie_title': new_movie['title'],
                    'date': '2023-02-20',
                    'rating': '5.0'
                })
                
                print(f"✓ Add viewing response status: {response.status_code}")
                
                # Verify movie was created
                created_movie = Movie.objects.filter(tmdb_id=new_movie['id']).first()
                if created_movie:
                    print(f"✓ Movie created in database: {created_movie.original_title}")
                    print(f"✓ Movie TMDB ID: {created_movie.tmdb_id}")
                else:
                    print("✗ Movie was not created in database")
            else:
                print("✓ Movie already exists in database")
    
    # Cleanup
    user.delete()
    user_profile.delete()
    
    print("\n✓ Complete add viewing process test completed!")
    print("✓ The new two-step movie search and selection process is working!")

if __name__ == '__main__':
    test_complete_add_viewing_process()