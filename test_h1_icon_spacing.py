#!/usr/bin/env python3
"""
Test to verify that the h1 icon spacing has been adjusted correctly.
"""

import os
import re

def test_h1_icon_spacing():
    """Test that the popcorn-card has proper left padding for h1 icons."""
    
    css_file = "store/static/css/popcorn-theme.css"
    
    # Check if the file exists
    if not os.path.exists(css_file):
        print(f"❌ CSS file not found: {css_file}")
        return False
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for the popcorn-card style with proper left padding
    popcorn_card_pattern = r'\.popcorn-card\s*\{[^}]*padding:\s*1\.5rem\s+1\.5rem\s+1\.5rem\s+3rem;[^}]*\}'
    
    # Test: Check that popcorn-card has proper padding (1.5rem top/right/bottom, 3rem left)
    if not re.search(popcorn_card_pattern, css_content):
        print("❌ Popcorn-card padding not found or not set correctly")
        return False
    
    print("✅ Popcorn-card has proper left padding (3rem) for h1 icons")
    
    # Check that h1::before still has the popcorn icon
    h1_before_pattern = r'h1::before\s*\{[^}]*content:\s*\'🍿\';[^}]*left:\s*-40px;[^}]*\}'
    if not re.search(h1_before_pattern, css_content):
        print("❌ h1::before popcorn icon not found or not positioned correctly")
        return False
    
    print("✅ h1::before popcorn icon is correctly positioned")
    
    print("\n🎉 h1 icon spacing test passed!")
    print("   Popcorn-card now has proper left padding to accommodate the 🍿 icon.")
    print("   The icon will be visible and properly spaced from the card edge.")
    
    return True

if __name__ == "__main__":
    success = test_h1_icon_spacing()
    exit(0 if success else 1)