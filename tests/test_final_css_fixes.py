#!/usr/bin/env python3
"""
Final comprehensive test for all CSS fixes implemented.
This test verifies that all the CSS improvements are properly applied.
"""

import os
import re

def test_all_css_fixes():
    """Test all CSS fixes comprehensively."""
    
    print("🎬 Testing all CSS fixes...")
    print("=" * 50)
    
    css_file = "store/static/css/popcorn-theme.css"
    template_files = [
        "store/templates/base.html",
        "store/templates/add_viewing.html"
    ]
    
    all_passed = True
    
    # Test 1: Navigation Icon Visibility Fix
    print("\n1. Testing Navigation Icon Visibility Fix...")
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Check active link icon fix
        if re.search(r'nav a\.active i\s*\{[^}]*color:\s*var\(--popcorn-red\);[^}]*\}', css_content):
            print("   ✅ Active nav icons are red for visibility")
        else:
            print("   ❌ Active nav icons fix not found")
            all_passed = False
    else:
        print("   ❌ CSS file not found")
        all_passed = False
    
    # Test 2: Popcorn Card Padding Adjustment
    print("\n2. Testing Popcorn Card Padding...")
    if os.path.exists(css_file):
        if re.search(r'\.popcorn-card\s*\{[^}]*padding:\s*1\.5rem\s+1\.5rem\s+1\.5rem\s+3rem;[^}]*\}', css_content):
            print("   ✅ Popcorn-card has proper padding (1.5rem, 3rem left)")
        else:
            print("   ❌ Popcorn-card padding not set correctly")
            all_passed = False
    
    # Test 3: H1 Icon Spacing
    print("\n3. Testing H1 Icon Spacing...")
    if os.path.exists(css_file):
        # Check that h1 icons are still positioned correctly
        if re.search(r'h1::before\s*\{[^}]*left:\s*-40px;[^}]*\}', css_content):
            print("   ✅ H1 icons are correctly positioned")
        else:
            print("   ❌ H1 icon positioning not found")
            all_passed = False
    
    # Test 4: Add Viewing Form Uses Popcorn Card
    print("\n4. Testing Add Viewing Form Integration...")
    add_viewing_template = "store/templates/add_viewing.html"
    if os.path.exists(add_viewing_template):
        with open(add_viewing_template, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check both containers use popcorn-card
        search_container = re.search(r'id="movie-search-container".*class="[^"]*popcorn-card[^"]*"', template_content)
        form_container = re.search(r'id="viewing-form-container".*class="[^"]*popcorn-card[^"]*"', template_content)
        
        if search_container and form_container:
            print("   ✅ Both form containers use popcorn-card class")
        else:
            print("   ❌ Form containers don't use popcorn-card class")
            all_passed = False
    else:
        print("   ❌ Add viewing template not found")
        all_passed = False
    
    # Test 5: Template Integration
    print("\n5. Testing Template Integration...")
    base_template = "store/templates/base.html"
    if os.path.exists(base_template):
        with open(base_template, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Check that popcorn-theme.css is loaded
        if '{% static \'css/popcorn-theme.css\' %}' in base_content:
            print("   ✅ Base template loads popcorn-theme.css")
        else:
            print("   ❌ Base template doesn't load popcorn-theme.css")
            all_passed = False
    else:
        print("   ❌ Base template not found")
        all_passed = False
    
    # Test 6: Responsive Design
    print("\n6. Testing Responsive Design...")
    if os.path.exists(css_file):
        if re.search(r'@media\s*\(max-width:', css_content):
            print("   ✅ Responsive media queries are present")
        else:
            print("   ❌ No responsive media queries found")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CSS FIXES TESTS PASSED!")
        print("\nSummary of fixes applied:")
        print("  • Navigation icons are visible on active links (red on gold)")
        print("  • Popcorn cards have compact padding with extra left space for icons")
        print("  • H1 popcorn icons have proper spacing from card edges")
        print("  • Add viewing forms use popcorn-card for consistent styling")
        print("  • All templates properly integrate the theme CSS")
        print("  • Responsive design is maintained")
        print("\n✅ The application now has a professional, consistent look!")
    else:
        print("❌ Some tests failed. Please review the CSS fixes.")
    
    return all_passed

if __name__ == "__main__":
    success = test_all_css_fixes()
    exit(0 if success else 1)