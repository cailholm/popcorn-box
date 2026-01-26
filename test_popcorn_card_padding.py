#!/usr/bin/env python3
"""
Test to verify that the popcorn-card padding has been adjusted correctly.
"""

import os
import re

def test_popcorn_card_padding():
    """Test that the popcorn-card padding has been reduced to 1.5rem."""
    
    css_file = "store/static/css/popcorn-theme.css"
    
    # Check if the file exists
    if not os.path.exists(css_file):
        print(f"❌ CSS file not found: {css_file}")
        return False
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for the popcorn-card style with correct padding
    popcorn_card_pattern = r'\.popcorn-card\s*\{[^}]*padding:\s*1\.5rem;[^}]*\}'
    
    # Test: Check that popcorn-card has 1.5rem padding
    if not re.search(popcorn_card_pattern, css_content):
        print("❌ Popcorn-card padding not found or not set to 1.5rem")
        return False
    
    print("✅ Popcorn-card padding is correctly set to 1.5rem")
    
    # Additional test: Make sure it's not still 2rem
    old_padding_pattern = r'\.popcorn-card\s*\{[^}]*padding:\s*2rem;[^}]*\}'
    if re.search(old_padding_pattern, css_content):
        print("❌ Old padding of 2rem still found - should be 1.5rem")
        return False
    
    print("✅ Old padding of 2rem has been removed")
    
    print("\n🎉 Popcorn-card padding test passed!")
    print("   Cards will now have more compact spacing while maintaining good visual appeal.")
    
    return True

if __name__ == "__main__":
    success = test_popcorn_card_padding()
    exit(0 if success else 1)