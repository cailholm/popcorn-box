#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from store.models import UserProfile
from django.utils import translation

def test_site_functionality():
    print("=== Test de fonctionnalité du site ===")
    print()
    
    # Create test client
    client = Client()
    
    # Test 1: Accès à la page de login
    print("Test 1: Accès à la page de login")
    try:
        response = client.get('/login/')
        print(f"  Statut: {response.status_code}")
        print(f"  Résultat: {'OK' if response.status_code == 200 else 'Échec'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Test 2: Créer un utilisateur et se connecter
    print("Test 2: Création d'utilisateur et connexion")
    try:
        # Créer un utilisateur
        user = User.objects.create_user(username='testuser5', email='test5@example.com', password='testpass123')
        user_profile = UserProfile.objects.create(user=user, language='es')
        
        print(f"  Utilisateur créé: {user.email}")
        print(f"  Langue: {user_profile.language}")
        
        # Se connecter
        login_success = client.login(username='testuser5', password='testpass123')
        print(f"  Connexion: {'OK' if login_success else 'Échec'}")
        
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Test 3: Accès à la page movies (nécessite authentification)
    print("Test 3: Accès à la page movies")
    try:
        response = client.get('/movies/')
        print(f"  Statut: {response.status_code}")
        if response.status_code == 200:
            print(f"  Contenu: {'OK' if b'Movie List' in response.content or b'Lista de' in response.content else 'Échec'}")
        else:
            print(f"  Redirection: {response.status_code}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Test 4: Vérification de la langue dans la session
    print("Test 4: Vérification de la langue dans la session")
    try:
        # Accéder à une page pour déclencher le middleware
        response = client.get('/movies/')
        
        # Vérifier la session
        session_language = client.session.get('_language', 'Non définie')
        print(f"  Langue dans la session: {session_language}")
        print(f"  Résultat: {'OK' if session_language == 'es' else 'Échec'}")
        
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Test 5: Déconnexion
    print("Test 5: Déconnexion")
    try:
        client.logout()
        response = client.get('/login/')
        print(f"  Statut après déconnexion: {response.status_code}")
        print(f"  Résultat: {'OK' if response.status_code == 200 else 'Échec'}")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    print()
    
    # Cleanup
    try:
        user_profile.delete()
        user.delete()
        print("Nettoyage effectué.")
    except:
        pass
    
    print("=== Test terminé ===")

if __name__ == '__main__':
    test_site_functionality()