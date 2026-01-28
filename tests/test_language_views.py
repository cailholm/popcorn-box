#!/usr/bin/env python

import os
import sys
import django

# Ajouter le chemin du projet au path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import TestCase, Client
from django.utils import translation
from django.contrib.auth.models import User
from store.models import UserProfile

class LanguageDetectionTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_home_page_french(self):
        """Test que la page d'accueil s'affiche en français lorsque le navigateur est en français"""
        print("Test: Page d'accueil en français")
        
        # Simuler un navigateur avec Accept-Language: fr
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
        
        print(f"Status code: {response.status_code}")
        print(f"Langue active: {translation.get_language()}")
        
        # Vérifier que la page contient du texte en français
        self.assertContains(response, 'Bienvenue sur Popcorn Box!')
        self.assertContains(response, 'Suivez tous les films que vous regardez')
        
        # Vérifier que la langue est définie dans le template
        self.assertContains(response, 'lang="fr"')
        
    def test_login_page_french(self):
        """Test que la page de login s'affiche en français lorsque le navigateur est en français"""
        print("\nTest: Page de login en français")
        
        # Simuler un navigateur avec Accept-Language: fr
        response = self.client.get('/login/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
        
        print(f"Status code: {response.status_code}")
        print(f"Langue active: {translation.get_language()}")
        
        # Vérifier que la page contient du texte en français
        self.assertContains(response, 'Se connecter')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Mot de passe:')
        
        # Vérifier que la langue est définie dans le template
        self.assertContains(response, 'lang="fr"')
        
    def test_home_page_spanish(self):
        """Test que la page d'accueil s'affiche en espagnol lorsque le navigateur est en espagnol"""
        print("\nTest: Page d'accueil en espagnol")
        
        # Simuler un navigateur avec Accept-Language: es
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='es-ES,es;q=0.9')
        
        print(f"Status code: {response.status_code}")
        print(f"Langue active: {translation.get_language()}")
        
        # Vérifier que la page contient du texte en espagnol
        self.assertContains(response, '¡Bienvenido a Popcorn Box!')
        self.assertContains(response, 'Registra todas las películas que ves')
        
        # Vérifier que la langue est définie dans le template
        self.assertContains(response, 'lang="es"')
        
    def test_login_page_spanish(self):
        """Test que la page de login s'affiche en espagnol lorsque le navigateur est en espagnol"""
        print("\nTest: Page de login en espagnol")
        
        # Simuler un navigateur avec Accept-Language: es
        response = self.client.get('/login/', HTTP_ACCEPT_LANGUAGE='es-ES,es;q=0.9')
        
        print(f"Status code: {response.status_code}")
        print(f"Langue active: {translation.get_language()}")
        
        # Vérifier que la page contient du texte en espagnol
        self.assertContains(response, 'Iniciar sesión')
        self.assertContains(response, 'Correo electrónico:')
        self.assertContains(response, 'Contraseña:')
        
        # Vérifier que la langue est définie dans le template
        self.assertContains(response, 'lang="es"')

if __name__ == '__main__':
    # Exécuter les tests
    import unittest
    
    suite = unittest.TestLoader().loadTestsFromTestCase(LanguageDetectionTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Afficher un résumé
    print(f"\n{'='*50}")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Succès: {result.wasSuccessful()}")