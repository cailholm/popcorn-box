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

def test_simple_template():
    """Test avec un template simplifié"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST: TEMPLATE SIMPLIFIÉ")
    print("=" * 60)
    
    # Créer un utilisateur de test
    username = f'testuser_{uuid.uuid4().hex[:8]}'
    user = User.objects.create_user(username=username, email=f'{username}@example.com', password='testpass123')
    UserProfile.objects.create(user=user, language='en')
    
    # Test 1: Utilisateur non connecté
    print("\n1. Utilisateur non connecté")
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier l'état d'authentification
    if 'data-user-authenticated="False"' in content or 'NON CONNECTÉ' in content:
        print("✓ Utilisateur non connecté détecté")
    else:
        print("✗ Utilisateur non connecté non détecté")
    
    # Test 2: Utilisateur connecté
    print("\n2. Utilisateur connecté")
    client.login(email=f'{username}@example.com', password='testpass123')
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier l'état d'authentification
    if 'data-user-authenticated="True"' in content or 'CONNECTÉ' in content:
        print("✓ Utilisateur connecté détecté")
    else:
        print("✗ Utilisateur connecté non détecté")
    
    # Vérifier les boutons
    if 'Movie List' in content or 'Liste des films' in content:
        print("✓ Boutons connectés présents")
    else:
        print("✗ Boutons connectés absents")
    
    # Vérifier si le problème vient du middleware
    print("\n3. Test sans middleware personnalisé")
    
    # Désactiver temporairement notre middleware en modifiant la configuration
    from django.conf import settings
    original_middleware = settings.MIDDLEWARE.copy()
    
    # Supprimer notre middleware
    settings.MIDDLEWARE = [mw for mw in settings.MIDDLEWARE if mw != 'store.middleware.UserLanguageMiddleware']
    
    # Recharger le client
    client2 = Client()
    client2.login(email=f'{username}@example.com', password='testpass123')
    response = client2.get('/')
    content = response.content.decode('utf-8')
    
    if 'Movie List' in content or 'Liste des films' in content:
        print("✓ Boutons connectés présents (sans middleware)")
    else:
        print("✗ Boutons connectés absents (sans middleware)")
    
    # Restaurer la configuration originale
    settings.MIDDLEWARE = original_middleware
    
    # Nettoyage
    client.logout()
    client2.logout()
    user.delete()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_simple_template()