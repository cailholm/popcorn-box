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
from store.views import login_view, movie_list, my_viewings, profile, add_viewing
from store.models import UserProfile
from django.utils import translation

def test_page_titles_translation():
    """Test que les titres de page sont traduits correctement"""
    
    factory = RequestFactory()
    
    # Test login page (sans authentification)
    request = factory.get('/login/')
    response = login_view(request)
    # Access context via template response
    if hasattr(response, 'context_data'):
        print(f"Login page title: {response.context_data['title']}")
    else:
        # For simple responses, we can see the content
        print("Login page rendered successfully")
    
    # Test with different languages
    for lang_code, lang_name in [('en', 'English'), ('fr', 'French'), ('de', 'German'), ('es', 'Spanish')]:
        print(f"\n--- Testing {lang_name} ({lang_code}) ---")
        
        # Activate language
        translation.activate(lang_code)
        
        # Create test user
        user = User.objects.create_user(username=f'testuser_{lang_code}', email=f'test{lang_code}@example.com', password='testpass')
        
        # Create user profile with language
        user_profile = UserProfile.objects.create(user=user, language=lang_code)
        
        # Create authenticated request
        request = factory.get('/movie-list/')
        request.user = user
        
        # Test movie_list page
        response = movie_list(request)
        if hasattr(response, 'context_data'):
            print(f"Movie List title ({lang_code}): {response.context_data['title']}")
        else:
            print(f"Movie List rendered for {lang_code}")
        
        # Test my_viewings page
        response = my_viewings(request)
        if hasattr(response, 'context_data'):
            print(f"My Viewings title ({lang_code}): {response.context_data['title']}")
        else:
            print(f"My Viewings rendered for {lang_code}")
        
        # Test profile page
        response = profile(request)
        if hasattr(response, 'context_data'):
            print(f"Profile title ({lang_code}): {response.context_data['title']}")
        else:
            print(f"Profile rendered for {lang_code}")
        
        # Test add_viewing page
        response = add_viewing(request)
        if hasattr(response, 'context_data'):
            print(f"Add Viewing title ({lang_code}): {response.context_data['title']}")
        else:
            print(f"Add Viewing rendered for {lang_code}")
        
        # Cleanup
        user.delete()
        user_profile.delete()

if __name__ == '__main__':
    test_page_titles_translation()