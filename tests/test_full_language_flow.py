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
from django.middleware.locale import LocaleMiddleware
from store.middleware import UserLanguageMiddleware

def test_full_language_flow():
    """Test du flux complet de détection de langue avec LocaleMiddleware et UserLanguageMiddleware"""
    
    # Créer une factory de requêtes
    factory = RequestFactory()
    
    # Créer une réponse factice
    from django.http import HttpResponse
    
    def get_response(request):
        return HttpResponse("")
    
    print("Test 1: Flux complet pour un utilisateur non authentifié avec navigateur en français")
    
    # Créer une requête avec en-tête Accept-Language
    request = factory.get('/')
    request.META['HTTP_ACCEPT_LANGUAGE'] = 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    request.session = {}
    request.user = django.contrib.auth.models.AnonymousUser()
    
    print(f"Langue initiale: {translation.get_language()}")
    
    # Appliquer LocaleMiddleware (celui de Django)
    locale_middleware = LocaleMiddleware(get_response)
    response = locale_middleware(request)
    
    print(f"Langue après LocaleMiddleware: {translation.get_language()}")
    
    # Appliquer UserLanguageMiddleware (le nôtre)
    user_lang_middleware = UserLanguageMiddleware(get_response)
    response = user_lang_middleware(request)
    
    print(f"Langue après UserLanguageMiddleware: {translation.get_language()}")
    print(f"Langue dans la session: {request.session.get('_language', 'non définie')}")
    
    print("\nTest 2: Flux complet pour un utilisateur non authentifié avec navigateur en espagnol")
    
    # Réinitialiser la langue
    translation.deactivate_all()
    
    request2 = factory.get('/')
    request2.META['HTTP_ACCEPT_LANGUAGE'] = 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7'
    request2.session = {}
    request2.user = django.contrib.auth.models.AnonymousUser()
    
    print(f"Langue initiale: {translation.get_language()}")
    
    # Appliquer LocaleMiddleware
    locale_middleware = LocaleMiddleware(get_response)
    response = locale_middleware(request2)
    
    print(f"Langue après LocaleMiddleware: {translation.get_language()}")
    
    # Appliquer UserLanguageMiddleware
    user_lang_middleware = UserLanguageMiddleware(get_response)
    response = user_lang_middleware(request2)
    
    print(f"Langue après UserLanguageMiddleware: {translation.get_language()}")
    print(f"Langue dans la session: {request2.session.get('_language', 'non définie')}")
    
    print("\nTest 3: Flux complet pour un utilisateur non authentifié avec navigateur en allemand")
    
    # Réinitialiser la langue
    translation.deactivate_all()
    
    request3 = factory.get('/')
    request3.META['HTTP_ACCEPT_LANGUAGE'] = 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    request3.session = {}
    request3.user = django.contrib.auth.models.AnonymousUser()
    
    print(f"Langue initiale: {translation.get_language()}")
    
    # Appliquer LocaleMiddleware
    locale_middleware = LocaleMiddleware(get_response)
    response = locale_middleware(request3)
    
    print(f"Langue après LocaleMiddleware: {translation.get_language()}")
    
    # Appliquer UserLanguageMiddleware
    user_lang_middleware = UserLanguageMiddleware(get_response)
    response = user_lang_middleware(request3)
    
    print(f"Langue après UserLanguageMiddleware: {translation.get_language()}")
    print(f"Langue dans la session: {request3.session.get('_language', 'non définie')}")

if __name__ == '__main__':
    test_full_language_flow()