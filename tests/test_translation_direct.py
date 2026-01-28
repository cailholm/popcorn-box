#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.utils import translation
from django.utils.translation import gettext as _

def test_translation_direct():
    """Test direct des traductions"""
    
    print("Testing direct translations:")
    
    # Test with different languages
    for lang_code, lang_name in [('en', 'English'), ('fr', 'French'), ('de', 'German'), ('es', 'Spanish')]:
        print(f"\n--- {lang_name} ({lang_code}) ---")
        
        # Activate language
        translation.activate(lang_code)
        
        # Tester les traductions
        print(f"Welcome to Popcorn Box: {_('Welcome to Popcorn Box')}")
        print(f"Movie List: {_('Movie List')}")
        print(f"My Viewings: {_('My Viewings')}")
        print(f"Profile: {_('Profile')}")
        print(f"Add Viewing: {_('Add Viewing')}")

if __name__ == '__main__':
    test_translation_direct()