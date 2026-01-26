#!/usr/bin/env python3
"""
Test to verify that the navigation icon visibility issue is fixed.
This test checks that active nav links have visible icons (red on gold background).
"""

import os
import re

def test_nav_icon_fix():
    """Test that the CSS fix for nav icon visibility is present."""
    
    css_file = "store/static/css/popcorn-theme.css"
    
    # Check if the file exists
    if not os.path.exists(css_file):
        print(f"❌ CSS file not found: {css_file}")
        return False
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for the active link style
    active_link_pattern = r'nav a\.active\s*\{[^}]*background-color:\s*var\(--popcorn-gold\);[^}]*\}'
    
    # Check for the icon fix
    icon_fix_pattern = r'nav a\.active i\s*\{[^}]*color:\s*var\(--popcorn-red\);[^}]*\}'
    
    # Test 1: Check that active link has gold background
    if not re.search(active_link_pattern, css_content):
        print("❌ Active link style not found or doesn't have gold background")
        return False
    
    print("✅ Active link has gold background")
    
    # Test 2: Check that active link icon has red color
    if not re.search(icon_fix_pattern, css_content):
        print("❌ Active link icon fix not found - icons will be invisible!")
        return False
    
    print("✅ Active link icon has red color for visibility")
    
    # Test 3: Check that regular icons are gold
    regular_icon_pattern = r'\.popcorn-icon\s*\{[^}]*color:\s*var\(--popcorn-gold\);[^}]*\}'
    if not re.search(regular_icon_pattern, css_content):
        print("❌ Regular popcorn-icon style not found")
        return False
    
    print("✅ Regular icons are gold as expected")
    
    # Test 4: Verify the fix is in the right place (after active link style)
    active_match = re.search(active_link_pattern, css_content)
    icon_match = re.search(icon_fix_pattern, css_content)
    
    if active_match and icon_match:
        active_pos = active_match.start()
        icon_pos = icon_match.start()
        
        # The icon fix should come after the active link style
        if icon_pos > active_pos:
            print("✅ Icon fix is properly placed after active link style")
        else:
            print("⚠️  Icon fix is before active link style (should work but unusual)")
    
    print("\n🎉 All tests passed! The navigation icon visibility issue is fixed.")
    print("   Active links will now have red icons on gold background for good contrast.")
    
    return True

if __name__ == "__main__":
    success = test_nav_icon_fix()
    exit(0 if success else 1)