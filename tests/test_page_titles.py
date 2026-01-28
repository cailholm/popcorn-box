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
from store.views import login_view, movie_list, my_viewings, profile, add_viewing
from store.models import UserProfile
from django.utils import translation

def test_page_titles_translation():
    """Test que les titres de page sont traduits correctement"""
    
    # Create test client
    client = Client()
    
    # Test login page (sans authentification)
    response = client.get('/login/')
    print(f"Login page title: {response.context['title']}")
    
    # Test with different languages
    for lang_code, lang_name in [('en', 'English'), ('fr', 'French'), ('de', 'German'), ('es', 'Spanish')]:
        print(f"\n--- Testing {lang_name} ({lang_code}) ---")
        
        # Activate language
        translation.activate(lang_code)
        
        # Create test user
        user = User.objects.create_user(username=f'testuser_{lang_code}', email=f'test{lang_code}@example.com', password='testpass')
        
        # Create user profile with language
        user_profile = UserProfile.objects.create(user=user, language=lang_code)
        
        # Login user
        client.force_login(user)
        
        # Test movie_list page
        response = client.get('/movie-list/')
        print(f"Movie List title ({lang_code}): {response.context['title']}")
        
        # Test my_viewings page
        response = client.get('/my-viewings/')
        print(f"My Viewings title ({lang_code}): {response.context['title']}")
        
        # Test profile page
        response = client.get('/profile/')
        print(f"Profile title ({lang_code}): {response.context['title']}")
        
        # Test add_viewing page
        response = client.get('/add-viewing/')
        print(f"Add Viewing title ({lang_code}): {response.context['title']}")
        
        # Logout
        client.logout()
        
        # Cleanup
        user.delete()
        user_profile.delete()

if __name__ == '__main__':
    test_page_titles_translation()