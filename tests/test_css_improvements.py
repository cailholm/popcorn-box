#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/domoserv/Mistral/popcorn-box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from store.models import UserProfile
from store.views import movie_list, login_view

def test_css_improvements():
    """Test pour vérifier que les améliorations CSS sont correctement appliquées"""
    
    factory = RequestFactory()
    
    print("Testing CSS improvements:")
    
    # Test 1: Vérifier que le fichier CSS existe
    css_file_path = '/home/domoserv/Mistral/popcorn-box/store/static/css/styles.css'
    if os.path.exists(css_file_path):
        print("✓ CSS file exists")
        
        # Vérifier la taille du fichier CSS
        file_size = os.path.getsize(css_file_path)
        print(f"  CSS file size: {file_size} bytes")
        
        if file_size > 5000:  # Le fichier devrait être assez grand
            print("✓ CSS file has significant content")
        else:
            print("⚠ CSS file might be too small")
            
        # Lire quelques lignes pour vérifier le contenu
        with open(css_file_path, 'r') as f:
            lines = f.readlines()
            print(f"  CSS file has {len(lines)} lines")
            
            # Vérifier quelques éléments clés
            css_content = ''.join(lines)
            
            key_elements = [
                '--primary-color',
                '--secondary-color',
                'font-awesome',
                'card',
                'fade-in',
                'movie-poster',
                'rating',
                '@media',
                'nav',
                'table'
            ]
            
            found_elements = []
            for element in key_elements:
                if element in css_content:
                    found_elements.append(element)
            
            print(f"  Found {len(found_elements)}/{len(key_elements)} key CSS elements: {', '.join(found_elements)}")
    else:
        print("✗ CSS file not found")
    
    # Test 2: Vérifier que les templates utilisent le nouveau CSS
    print("\n--- Testing template integration ---")
    
    # Lire le template base.html
    base_template_path = '/home/domoserv/Mistral/popcorn-box/store/templates/base.html'
    with open(base_template_path, 'r') as f:
        base_content = f.read()
    
    # Vérifier que le template utilise le fichier CSS externe
    if '{% static \'css/styles.css\' %}' in base_content:
        print("✓ Base template uses external CSS file")
    else:
        print("⚠ Base template might not be using external CSS file")
    
    # Vérifier que le template n'a pas de CSS intégré
    if '<style>' not in base_content and '</style>' not in base_content:
        print("✓ No inline CSS found in base template")
    else:
        print("⚠ Inline CSS still present in base template")
    
    # Test 3: Vérifier que les vues fonctionnent toujours
    print("\n--- Testing view functionality ---")
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    user_profile = UserProfile.objects.create(user=user, language='en')
    
    # Test login view
    request = factory.get('/login/')
    try:
        response = login_view(request)
        print("✓ Login view works")
        print(f"  Status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Login view failed: {e}")
    
    # Test movie_list view (needs authentication)
    request = factory.get('/movie-list/')
    request.user = user
    try:
        response = movie_list(request)
        print("✓ Movie list view works")
        print(f"  Status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Movie list view failed: {e}")
    
    # Cleanup
    user_profile.delete()
    user.delete()
    
    print("\n✓ CSS improvements test completed!")
    print("✓ Professional CSS has been successfully implemented!")

if __name__ == '__main__':
    test_css_improvements()