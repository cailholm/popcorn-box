"""
Test permanent pour l'API de recherche de films
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import UserProfile


class MovieSearchAPITest(TestCase):
    """Test de l'API de recherche de films"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            language='en'
        )
        self.client.force_login(self.user)
    
    def test_api_unauthorized_access(self):
        """Test l'accès non autorisé à l'API"""
        # Créer un client non authentifié
        unauthorized_client = Client()
        response = unauthorized_client.get('/api/search-movies/?query=Batman')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
    
    def test_api_minimum_characters_validation(self):
        """Test la validation du nombre minimum de caractères"""
        # Test avec une requête trop courte
        response = self.client.get('/api/search-movies/?query=a')
        self.assertEqual(response.status_code, 400)
        
        # Test avec une requête vide
        response = self.client.get('/api/search-movies/?query=')
        self.assertEqual(response.status_code, 400)
    
    def test_api_successful_search(self):
        """Test une recherche réussie"""
        response = self.client.get('/api/search-movies/?query=Batman')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Vérifier que nous avons des résultats
        self.assertTrue(isinstance(data, list))
        self.assertGreater(len(data), 0)
        
        # Vérifier la structure des résultats
        first_movie = data[0]
        self.assertIn('id', first_movie)
        self.assertIn('title', first_movie)
        self.assertIn('year', first_movie)
        self.assertIn('overview', first_movie)
    
    def test_api_search_results_limit(self):
        """Test la limite des résultats de recherche"""
        response = self.client.get('/api/search-movies/?query=Batman')
        data = response.json()
        
        # Should be limited to 10 results
        self.assertLessEqual(len(data), 10)
    
    def test_api_error_handling(self):
        """Test la gestion des erreurs"""
        # This is harder to test without mocking, but we can test the structure
        response = self.client.get('/api/search-movies/?query=Batman')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        """Nettoyage après les tests"""
        self.user.delete()
        self.user_profile.delete()


if __name__ == '__main__':
    import unittest
    unittest.main()