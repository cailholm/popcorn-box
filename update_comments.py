#!/usr/bin/env python3
"""
Script to update French comments to English in Python files
"""

import os
import re
import glob

# Common French to English comment translations
COMMENT_TRANSLATIONS = {
    # Configuration and setup
    r'# Add project path to sys.path': '# Add project path to sys.path',
    r'# Configure Django settings': '# Configure Django settings',
    r'# Django configuration': '# Django configuration',
    
    # Test setup
    r'# Create test client': '# Create test client',
    r'# Create test user': '# Create test user',
    r'# Create test movie': '# Create test movie',
    r'# Create viewing': '# Create viewing',
    r'# Connecter l\'utilisateur': '# Login user',
    
    # Test actions
    r'# Test translation logic directly': '# Test translation logic directly',
    r'# Simulate what movie_list view does': '# Simulate what movie_list view does',
    r'# Test translation logic for viewings': '# Test translation logic for viewings',
    r'# Test language change': '# Test language change',
    r'# Test login page': '# Test login page',
    r'# Test with different languages': '# Test with different languages',
    r'# Activate language': '# Activate language',
    r'# Create user profile with language': '# Create user profile with language',
    r'# Create authenticated request': '# Create authenticated request',
    r'# Test movie_list page': '# Test movie_list page',
    r'# Test my_viewings page': '# Test my_viewings page',
    r'# Test profile page': '# Test profile page',
    r'# Test add_viewing page': '# Test add_viewing page',
    r'# Logout': '# Logout',
    
    # Cleanup
    r'# Cleanup': '# Cleanup',
    r'# Cleanup': '# Cleanup',
    
    # Search functionality
    r'# Search for a movie': '# Search for a movie',
    r'# Verify JavaScript is present': '# Verify JavaScript is present',
    r'# Verify JavaScript structure': '# Verify JavaScript structure',
    r'# Verify translated messages are present': '# Verify translated messages are present',
    r'# Verify page contains fixed JavaScript': '# Verify page contains fixed JavaScript',
    r'# Verify messages are properly defined': '# Verify messages are properly defined',
    r'# Vérifier que l\'API fonctionne toujours': '# Verify API still works',
    
    # Translation specific
    r'# Test French translation': '# Test French translation',
    r'# Test Spanish translation': '# Test Spanish translation',
    r'# Tester la récupération d\'une traduction existante': '# Test retrieval of existing translation',
    
    # Additional translations found
    r'# Test search with different terms': '# Test search with different terms',
    r'# Step 1: Search for a movie': '# Step 1: Search for a movie',
    r'# Step 2: Add viewing': '# Step 2: Add viewing',
    r'# Verify viewing was created': '# Verify viewing was created',
    r'# Redirect after success': '# Redirect after success',
    r'# Changer la langue de l\'utilisateur': '# Change user language',
    r'# Tester la page d\'ajout de visionnage': '# Test add viewing page',
    r'# Test search': '# Test search',
    r'# Réactiver l\'anglais': '# Reactivate English',
    r'# Tester avec un film qui n\'a probablement pas d\'affiche': '# Test with a movie that probably has no poster',
    r'# Vérifier que l\'affiche est incluse': '# Verify poster is included',
    r'# Verify complete structure': '# Verify complete structure',
    r'# For simple responses, we can see the content': '# For simple responses, we can see the content',
    r'# Access context via template response': '# Access context via template response',
    r'# Create authenticated request': '# Create authenticated request',
    r'# Verify translation works': '# Verify translation works',
    r'# Verify translation is correct': '# Verify translation is correct',
    r'# Verify translation is properly applied': '# Verify translation is properly applied',
}

def update_file_comments(filepath):
    """Update comments in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply translations
        for french_pattern, english_comment in COMMENT_TRANSLATIONS.items():
            content = re.sub(french_pattern, english_comment, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"  No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to update comments in all Python test files"""
    print("🔧 Updating French comments to English...")
    print("=" * 50)
    
    # Find all Python test files
    python_files = glob.glob('test_*.py') + glob.glob('*.py')
    
    updated_count = 0
    total_files = len(python_files)
    
    for filepath in python_files:
        if update_file_comments(filepath):
            updated_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {updated_count}/{total_files} files updated")
    print("✅ Comment update process completed!")

if __name__ == '__main__':
    main()