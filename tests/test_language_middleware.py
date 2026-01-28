#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from store.models import UserProfile
from store.middleware import UserLanguageMiddleware
from django.utils import translation

def test_language_middleware():
    print("=== Test du middleware de langue ===")
    print()
    
    # Create test user
    user = User.objects.create_user(username='testuser3', email='test3@example.com', password='testpass123')
    user_profile = UserProfile.objects.create(user=user, language='es')  # Espagnol
    
    print(f"Utilisateur créé: {user.email}")
    print(f"Langue du profil: {user_profile.language}")
    print()
    
    # Créer un middleware et une requête factice
    middleware = UserLanguageMiddleware(lambda request: None)
    factory = RequestFactory()
    
    # Test 1: Requête sans utilisateur authentifié
    print("Test 1: Requête sans utilisateur authentifié")
    request = factory.get('/test/')
    request.user = User()  # Utilisateur non authentifié
    
    current_lang = translation.get_language()
    print(f"  Langue avant middleware: {current_lang}")
    
    middleware(request)
    
    new_lang = translation.get_language()
    print(f"  Langue après middleware: {new_lang}")
    print(f"  Résultat: {'OK' if current_lang == new_lang else 'Changement inattendu'}")
    print()
    
    # Test 2: Requête avec utilisateur authentifié (espagnol)
    print("Test 2: Requête avec utilisateur authentifié (espagnol)")
    request = factory.get('/test/')
    request.user = user
    request.session = {}  # Session vide
    
    # Réinitialiser la langue à anglais pour le test
    translation.activate('en')
    current_lang = translation.get_language()
    print(f"  Langue avant middleware: {current_lang}")
    
    middleware(request)
    
    new_lang = translation.get_language()
    print(f"  Langue après middleware: {new_lang}")
    print(f"  Résultat: {'OK' if new_lang == 'es' else 'Échec - devrait être espagnol'}")
    print(f"  Session langue: {request.session.get('_language', 'Non définie')}")
    print()
    
    # Test 3: Vérifier que la langue persiste
    print("Test 3: Vérification de la persistance de la langue")
    request = factory.get('/test/')
    request.user = user
    request.session = {'_language': 'es'}  # Session avec langue déjà définie
    
    current_lang = translation.get_language()
    print(f"  Langue actuelle: {current_lang}")
    
    middleware(request)
    
    new_lang = translation.get_language()
    print(f"  Langue après middleware: {new_lang}")
    print(f"  Résultat: {'OK' if new_lang == 'es' else 'Échec'}")
    print()
    
    # Test 4: Changement de langue dans le profil
    print("Test 4: Changement de langue dans le profil (français)")
    user_profile.language = 'fr'
    user_profile.save()
    
    # Réinitialiser la langue
    translation.activate('en')
    
    request = factory.get('/test/')
    request.user = user
    request.session = {}
    
    current_lang = translation.get_language()
    print(f"  Langue avant middleware: {current_lang}")
    
    middleware(request)
    
    new_lang = translation.get_language()
    print(f"  Langue après middleware: {new_lang}")
    print(f"  Résultat: {'OK' if new_lang == 'fr' else 'Échec - devrait être français'}")
    print()
    
    # Cleanup
    user_profile.delete()
    user.delete()
    
    print("=== Test terminé ===")
    print("Le middleware devrait maintenant activer correctement la langue de l'utilisateur")
    print("pour chaque requête, ce qui résoudra le problème des éléments de menu en français")
    print("alors que la langue de l'utilisateur est espagnol.")

if __name__ == '__main__':
    test_language_middleware()