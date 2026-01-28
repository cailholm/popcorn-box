#!/usr/bin/env python

import os
import sys
import django

# Ajouter le chemin du projet au path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import RequestFactory
from django.utils import translation
from store.middleware import UserLanguageMiddleware

def test_language_detection():
    """Test de la détection de langue du navigateur"""
    
    # Créer une factory de requêtes
    factory = RequestFactory()
    
    # Créer un middleware
    middleware = UserLanguageMiddleware(lambda request: None)
    
    print("Test 1: Utilisateur non authentifié avec en-tête Accept-Language: fr")
    request = factory.get('/')
    request.META['HTTP_ACCEPT_LANGUAGE'] = 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    request.session = {}
    request.user = django.contrib.auth.models.AnonymousUser()
    
    # Simuler le LocaleMiddleware qui devrait définir la langue
    translation.activate('fr')
    
    # Appeler le middleware
    middleware(request)
    
    print(f"Langue après middleware: {translation.get_language()}")
    print(f"Langue dans la session: {request.session.get('_language', 'non définie')}")
    
    print("\nTest 2: Utilisateur non authentifié avec en-tête Accept-Language: es")
    request2 = factory.get('/')
    request2.META['HTTP_ACCEPT_LANGUAGE'] = 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7'
    request2.session = {}
    request2.user = django.contrib.auth.models.AnonymousUser()
    
    # Simuler le LocaleMiddleware
    translation.activate('es')
    
    # Appeler le middleware
    middleware(request2)
    
    print(f"Langue après middleware: {translation.get_language()}")
    print(f"Langue dans la session: {request2.session.get('_language', 'non définie')}")
    
    print("\nTest 3: Utilisateur non authentifié avec en-tête Accept-Language: de")
    request3 = factory.get('/')
    request3.META['HTTP_ACCEPT_LANGUAGE'] = 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    request3.session = {}
    request3.user = django.contrib.auth.models.AnonymousUser()
    
    # Simuler le LocaleMiddleware
    translation.activate('de')
    
    # Appeler le middleware
    middleware(request3)
    
    print(f"Langue après middleware: {translation.get_language()}")
    print(f"Langue dans la session: {request3.session.get('_language', 'non définie')}")
    
    print("\nTest 4: Utilisateur non authentifié sans en-tête Accept-Language (langue par défaut)")
    request4 = factory.get('/')
    request4.session = {}
    request4.user = django.contrib.auth.models.AnonymousUser()
    
    # Simuler le LocaleMiddleware avec la langue par défaut
    translation.activate('en')
    
    # Appeler le middleware
    middleware(request4)
    
    print(f"Langue après middleware: {translation.get_language()}")
    print(f"Langue dans la session: {request4.session.get('_language', 'non définie')}")

if __name__ == '__main__':
    test_language_detection()