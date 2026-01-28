#!/usr/bin/env python

import os
import sys
import django

# Ajouter le chemin du projet au path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from store.models import UserProfile
import uuid

def test_correct_login():
    """Test avec la méthode de login correcte"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST: LOGIN CORRECT")
    print("=" * 60)
    
    # Créer un utilisateur de test
    username = f'testuser_{uuid.uuid4().hex[:8]}'
    user = User.objects.create_user(username=username, email=f'{username}@example.com', password='testpass123')
    UserProfile.objects.create(user=user, language='en')
    
    print(f"Utilisateur créé: {username}")
    
    # Test 1: Login avec username (méthode correcte)
    print("\n1. Login avec username")
    success = client.login(username=username, password='testpass123')
    print(f"Login réussi: {success}")
    
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier les boutons connectés
    if 'Movie List' in content or 'Liste des films' in content:
        print("✓ Boutons connectés présents (avec login par username)")
    else:
        print("✗ Boutons connectés absents (avec login par username)")
    
    # Vérifier les boutons non connectés
    if 'href="/login/"' in content or 'href="/signup/"' in content:
        print("✗ Boutons non connectés présents (incorrect)")
    else:
        print("✓ Boutons non connectés absents (correct)")
    
    # Déconnecter
    client.logout()
    
    # Test 2: Login avec email (méthode incorrecte)
    print("\n2. Login avec email")
    success = client.login(email=f'{username}@example.com', password='testpass123')
    print(f"Login réussi: {success}")
    
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier les boutons connectés
    if 'Movie List' in content or 'Liste des films' in content:
        print("✓ Boutons connectés présents (avec login par email)")
    else:
        print("✗ Boutons connectés absents (avec login par email)")
    
    # Nettoyage
    client.logout()
    user.delete()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_correct_login()