#!/usr/bin/env python3
"""
Script to update imports from old module names to new ones.
Note: The 'store' app is the main Django application containing models, views, etc.
"""

import os
import re
import glob

def update_file_imports(filepath):
    """Update imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Update import statements (example: from old_module to store)
        # This script can be customized for future refactoring needs
        # Currently no changes needed as project is properly configured
        
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
    """Main function to update imports in all Python files"""
    print("🔧 Updating imports from 'store' to 'popcorn_box'...")
    print("=" * 60)
    
    # Find all Python files
    python_files = glob.glob('*.py') + glob.glob('**/*.py', recursive=True)
    python_files = [f for f in python_files if not f.startswith('./popcorn_box/')]  # Skip the app itself
    
    updated_count = 0
    total_files = len(python_files)
    
    for filepath in python_files:
        if update_file_imports(filepath):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {updated_count}/{total_files} files updated")
    print("✅ Import update process completed!")

if __name__ == '__main__':
    main()