#!/usr/bin/env python3
"""
Test to verify that the my_viewings page typography has been adjusted correctly.
"""

import os
import re

def test_my_viewings_typography():
    """Test that my_viewings page has proper typography."""
    
    css_file = "store/static/css/popcorn-theme.css"
    
    print("🎬 Testing My Viewings Typography...")
    print("=" * 50)
    
    all_passed = True
    
    # Check if the file exists
    if not os.path.exists(css_file):
        print("❌ CSS file not found")
        return False
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Test 1: Date title size (should be 1.2rem, not 1.4rem)
    print("\n1. Testing Date Title Size...")
    date_title_pattern = r'\.viewing-date-title\s*\{[^}]*font-size:\s*1\.2rem;[^}]*\}'
    if re.search(date_title_pattern, css_content):
        print("   ✅ Date titles are 1.2rem (reduced from 1.4rem)")
    else:
        print("   ❌ Date title size not set correctly")
        all_passed = False
    
    # Test 2: Date title weight (should be 700, not 800)
    date_weight_pattern = r'\.viewing-date-title\s*\{[^}]*font-weight:\s*700;[^}]*\}'
    if re.search(date_weight_pattern, css_content):
        print("   ✅ Date title weight is 700 (reduced from 800)")
    else:
        print("   ❌ Date title weight not set correctly")
        all_passed = False
    
    # Test 3: Movie title size (should be 1.3rem, not 1.1rem)
    print("\n2. Testing Movie Title Size...")
    movie_title_pattern = r'\.viewing-movie-title\s*\{[^}]*font-size:\s*1\.3rem;[^}]*\}'
    if re.search(movie_title_pattern, css_content):
        print("   ✅ Movie titles are 1.3rem (increased from 1.1rem)")
    else:
        print("   ❌ Movie title size not set correctly")
        all_passed = False
    
    # Test 4: Movie title weight (should be 600)
    movie_weight_pattern = r'\.viewing-movie-title\s*\{[^}]*font-weight:\s*600;[^}]*\}'
    if re.search(movie_weight_pattern, css_content):
        print("   ✅ Movie title weight is 600")
    else:
        print("   ❌ Movie title weight not set correctly")
        all_passed = False
    
    # Test 5: Movie meta size (should be 1rem, not 0.9rem)
    print("\n3. Testing Movie Meta Size...")
    movie_meta_pattern = r'\.viewing-movie-meta\s*\{[^}]*font-size:\s*1rem;[^}]*\}'
    if re.search(movie_meta_pattern, css_content):
        print("   ✅ Movie meta (year, director) is 1rem (increased from 0.9rem)")
    else:
        print("   ❌ Movie meta size not set correctly")
        all_passed = False
    
    # Test 6: Movie meta weight (should be 500)
    movie_meta_weight_pattern = r'\.viewing-movie-meta\s*\{[^}]*font-weight:\s*500;[^}]*\}'
    if re.search(movie_meta_weight_pattern, css_content):
        print("   ✅ Movie meta weight is 500")
    else:
        print("   ❌ Movie meta weight not set correctly")
        all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL MY VIEWINGS TYPOGRAPHY TESTS PASSED!")
        print("\nTypography adjustments applied:")
        print("  • Date titles: 1.2rem, weight 700 (more balanced)")
        print("  • Movie titles: 1.3rem, weight 600 (more prominent)")
        print("  • Movie meta: 1rem, weight 500 (more readable)")
        print("\n✅ My Viewings page now has better visual hierarchy!")
    else:
        print("❌ Some typography tests failed.")
    
    return all_passed

if __name__ == "__main__":
    success = test_my_viewings_typography()
    exit(0 if success else 1)