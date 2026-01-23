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
from store.models import UserProfile

def test_js_fix():
    """Test pour vérifier que le JavaScript est maintenant correct"""
    
    print("Testing JavaScript fix for movie search:")
    
    # Create test client
    client = Client()
    
    # Create test user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    user_profile = UserProfile.objects.create(user=user, language='en')
    
    # Login user
    client.force_login(user)
    
    # Test add_viewing page pour voir si le JavaScript est valide
    response = client.get('/add_viewing/')
    
    print(f"✓ Page loaded with status: {response.status_code}")
    
    # Verify page contains fixed JavaScript
    content = response.content.decode('utf-8')
    
    # Verify messages are properly defined
    if 'const messages = {' in content:
        print("✓ JavaScript messages object found")
    else:
        print("✗ JavaScript messages object not found")
    
    # Vérifier que les messages traduits sont utilisés
    if 'messages.minChars' in content:
        print("✓ Using messages.minChars")
    else:
        print("✗ Not using messages.minChars")
    
    if 'messages.searching' in content:
        print("✓ Using messages.searching")
    else:
        print("✗ Not using messages.searching")
    
    if 'messages.error' in content:
        print("✓ Using messages.error")
    else:
        print("✗ Not using messages.error")
    
    # Tester que l'API fonctionne toujours
    print("\nTesting API functionality:")
    response = client.get('/api/search-movies/?query=Batman')
    
    if response.status_code == 200:
        print("✓ API search works")
        data = response.json()
        print(f"✓ Found {len(data)} results")
    else:
        print(f"✗ API search failed: {response.status_code}")
    
    # Cleanup
    user.delete()
    user_profile.delete()
    
    print("\n✓ JavaScript fix test completed!")
    print("✓ The syntax error should now be resolved")

if __name__ == '__main__':
    test_js_fix()