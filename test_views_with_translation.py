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

def test_views_with_translation():
    """Test que les vues utilisent bien les traductions"""
    
    factory = RequestFactory()
    
    print("Testing views with translations:")
    
    # Test with different languages
    for lang_code, lang_name in [('en', 'English'), ('fr', 'French'), ('de', 'German'), ('es', 'Spanish')]:
        print(f"\n--- {lang_name} ({lang_code}) ---")
        
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
        # Extraire le titre du contexte
        if hasattr(response, 'render') and callable(response.render):
            # C'est un TemplateResponse, nous pouvons accéder au contexte
            context = response.render().context
            print(f"Movie List title: {context['title']}")
        elif hasattr(response, 'context_data'):
            print(f"Movie List title: {response.context_data['title']}")
        else:
            print("Movie List: Could not access context")
        
        # Test my_viewings page
        response = my_viewings(request)
        if hasattr(response, 'render') and callable(response.render):
            context = response.render().context
            print(f"My Viewings title: {context['title']}")
        elif hasattr(response, 'context_data'):
            print(f"My Viewings title: {response.context_data['title']}")
        else:
            print("My Viewings: Could not access context")
        
        # Test profile page
        response = profile(request)
        if hasattr(response, 'render') and callable(response.render):
            context = response.render().context
            print(f"Profile title: {context['title']}")
        elif hasattr(response, 'context_data'):
            print(f"Profile title: {response.context_data['title']}")
        else:
            print("Profile: Could not access context")
        
        # Test add_viewing page
        response = add_viewing(request)
        if hasattr(response, 'render') and callable(response.render):
            context = response.render().context
            print(f"Add Viewing title: {context['title']}")
        elif hasattr(response, 'context_data'):
            print(f"Add Viewing title: {response.context_data['title']}")
        else:
            print("Add Viewing: Could not access context")
        
        # Cleanup
        user.delete()
        user_profile.delete()

if __name__ == '__main__':
    test_views_with_translation()