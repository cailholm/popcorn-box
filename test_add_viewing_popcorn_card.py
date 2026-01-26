#!/usr/bin/env python3
"""
Test to verify that the add_viewing form is now using popcorn-card classes.
"""

import os
import re

def test_add_viewing_popcorn_card():
    """Test that the add_viewing template uses popcorn-card classes."""
    
    template_file = "store/templates/add_viewing.html"
    
    # Check if the file exists
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        return False
    
    # Read the template file
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Test 1: Check that movie-search-container has popcorn-card class
    search_container_pattern = r'id="movie-search-container".*class="[^"]*popcorn-card[^"]*"'
    if not re.search(search_container_pattern, template_content):
        print("❌ movie-search-container doesn't have popcorn-card class")
        return False
    
    print("✅ movie-search-container has popcorn-card class")
    
    # Test 2: Check that viewing-form-container has popcorn-card class
    form_container_pattern = r'id="viewing-form-container".*class="[^"]*popcorn-card[^"]*"'
    if not re.search(form_container_pattern, template_content):
        print("❌ viewing-form-container doesn't have popcorn-card class")
        return False
    
    print("✅ viewing-form-container has popcorn-card class")
    
    # Test 3: Check that the old background/box-shadow styles are removed from CSS
    # (They should not be in the extra_css since we're using popcorn-card now)
    old_styles_pattern = r'background:\s*white;.*padding:\s*1\.5rem;.*border-radius:\s*var\(--border-radius\);.*box-shadow:\s*var\(--box-shadow\);'
    if re.search(old_styles_pattern, template_content, re.DOTALL):
        print("❌ Old background/box-shadow styles still present in CSS")
        return False
    
    print("✅ Old redundant styles have been removed")
    
    # Test 4: Check that fade-in class is still present (for animations)
    fade_in_pattern = r'class="[^"]*fade-in[^"]*"'
    if not re.search(fade_in_pattern, template_content):
        print("⚠️  fade-in class not found (animations may not work)")
    else:
        print("✅ fade-in class is still present for animations")
    
    print("\n🎉 Add Viewing popcorn-card test passed!")
    print("   Both form containers now use popcorn-card for consistent styling.")
    print("   The forms will have the same visual style as other cards in the app.")
    
    return True

if __name__ == "__main__":
    success = test_add_viewing_popcorn_card()
    exit(0 if success else 1)