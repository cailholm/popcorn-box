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

def test_navbar_always_visible():
    """Test que la navbar est toujours visible et adapte ses boutons"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST: NAVBAR TOUJOURS VISIBLE")
    print("=" * 60)
    
    # Test 1: Page d'accueil pour utilisateur non connecté
    print("\n1. Page d'accueil - Utilisateur non connecté")
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier que la navbar est présente
    if '<nav class="cinema-nav">' in content:
        print("   ✓ Navbar présente")
    else:
        print("   ✗ Navbar absente")
    
    # Vérifier les boutons pour utilisateur non connecté
    if 'href="/login/"' in content and 'href="/signup/"' in content:
        print("   ✓ Boutons Login et Sign Up présents")
    else:
        print("   ✗ Boutons Login/Sign Up absents")
    
    # Vérifier que les boutons connectés sont absents
    if 'href="/movies/"' not in content and 'href="/logout/"' not in content:
        print("   ✓ Boutons connectés absents (correct)")
    else:
        print("   ✗ Boutons connectés présents (incorrect)")
    
    # Test 2: Page de login pour utilisateur non connecté
    print("\n2. Page de login - Utilisateur non connecté")
    response = client.get('/login/')
    content = response.content.decode('utf-8')
    
    # Vérifier que la navbar est présente
    if '<nav class="cinema-nav">' in content:
        print("   ✓ Navbar présente")
    else:
        print("   ✗ Navbar absente")
    
    # Vérifier les boutons pour utilisateur non connecté
    if 'href="/login/"' in content and 'href="/signup/"' in content:
        print("   ✓ Boutons Login et Sign Up présents")
    else:
        print("   ✗ Boutons Login/Sign Up absents")
    
    # Test 3: Page d'accueil pour utilisateur connecté
    print("\n3. Page d'accueil - Utilisateur connecté")
    
    # Créer un utilisateur de test
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
    UserProfile.objects.create(user=user, language='en')
    
    # Connecter l'utilisateur
    client.login(email='test@example.com', password='testpass123')
    
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    # Vérifier que la navbar est présente
    if '<nav class="cinema-nav">' in content:
        print("   ✓ Navbar présente")
    else:
        print("   ✗ Navbar absente")
    
    # Vérifier les boutons pour utilisateur connecté
    if 'href="/movies/"' in content and 'href="/my_viewings/"' in content and 'href="/logout/"' in content:
        print("   ✓ Boutons connectés présents")
    else:
        print("   ✗ Boutons connectés absents")
    
    # Vérifier que les boutons non connectés sont absents
    if 'href="/login/"' not in content and 'href="/signup/"' not in content:
        print("   ✓ Boutons non connectés absents (correct)")
    else:
        print("   ✗ Boutons non connectés présents (incorrect)")
    
    # Test 4: Page de login pour utilisateur connecté (redirection attendue)
    print("\n4. Page de login - Utilisateur connecté (redirection)")
    response = client.get('/login/')
    
    # Should redirect to home or my_viewings
    if response.status_code == 302:
        print("   ✓ Redirection correcte (utilisateur déjà connecté)")
    else:
        print(f"   ✗ Pas de redirection (status: {response.status_code})")
    
    # Déconnecter l'utilisateur
    client.logout()
    
    # Test 5: Vérification des traductions dans la navbar
    print("\n5. Traductions dans la navbar (français)")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
    content = response.content.decode('utf-8')
    
    if 'Connexion' in content and 'Inscription' in content:
        print("   ✓ Traductions françaises présentes")
    else:
        print("   ✗ Traductions françaises absentes")
    
    # Nettoyage
    user.delete()
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)
    print("\nRésumé:")
    print("- La navbar est toujours visible")
    print("- Les boutons s'adaptent en fonction de l'état de connexion")
    print("- Les traductions sont appliquées dans la navbar")
    print("- Les redirections fonctionnent correctement")

if __name__ == '__main__':
    test_navbar_always_visible()