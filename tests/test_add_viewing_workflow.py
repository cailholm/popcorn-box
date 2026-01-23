"""
Test permanent pour le workflow complet d'ajout de visionnage
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import UserProfile, Movie, Viewing


class AddViewingWorkflowTest(TestCase):
    """Test du workflow complet d'ajout de visionnage"""
    
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
    
    def test_add_viewing_page_access(self):
        """Test l'accès à la page d'ajout de visionnage"""
        response = self.client.get('/add_viewing/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 1: Search for a movie')
        self.assertContains(response, 'Step 2: Add Viewing Details')
    
    def test_add_viewing_with_existing_movie(self):
        """Test l'ajout de visionnage avec un film existant"""
        # Créer un film existant
        movie = Movie.objects.create(
            original_title='Test Movie',
            year=2020,
            summary='A test movie',
            director='Test Director',
            original_language='en',
            tmdb_id=123456
        )
        
        # Ajouter un visionnage
        response = self.client.post('/add_viewing/', {
            'movie_id': movie.tmdb_id,
            'movie_title': movie.original_title,
            'date': '2023-01-15',
            'rating': '4.5'
        })
        
        # Should redirect to my_viewings
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/my_viewings/'))
        
        # Vérifier que le visionnage a été créé
        viewings = Viewing.objects.filter(user=self.user)
        self.assertEqual(viewings.count(), 1)
        
        viewing = viewings.first()
        self.assertEqual(viewing.movie, movie)
        self.assertEqual(str(viewing.date), '2023-01-15')
        self.assertEqual(float(viewing.rating), 4.5)
    
    def test_add_viewing_with_new_movie(self):
        """Test l'ajout de visionnage avec un nouveau film (via API TMDb)"""
        # Utiliser un ID TMDb connu pour le test
        tmdb_id = 157336  # Interstellar
        
        # Ajouter un visionnage avec un film qui n'existe pas encore
        response = self.client.post('/add_viewing/', {
            'movie_id': tmdb_id,
            'movie_title': 'Interstellar',
            'date': '2023-02-20',
            'rating': '5.0'
        })
        
        # Should redirect to my_viewings
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que le film a été créé
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        self.assertIsNotNone(movie)
        self.assertEqual(movie.original_title, 'Interstellar')
        
        # Vérifier que le visionnage a été créé
        viewings = Viewing.objects.filter(user=self.user)
        self.assertEqual(viewings.count(), 1)
        
        viewing = viewings.first()
        self.assertEqual(viewing.movie, movie)
    
    def test_add_viewing_form_validation(self):
        """Test la validation du formulaire"""
        # Soumettre un formulaire incomplet
        response = self.client.post('/add_viewing/', {
            'movie_id': '',
            'movie_title': '',
            'date': '',
            'rating': ''
        })
        
        # Should return to form with errors
        self.assertEqual(response.status_code, 200)
        
        # No viewings should be created
        viewings = Viewing.objects.filter(user=self.user)
        self.assertEqual(viewings.count(), 0)
    
    def test_multilingual_interface(self):
        """Test l'interface multilingue"""
        # Tester avec différentes langues
        languages = ['fr', 'de', 'es']
        
        for lang in languages:
            self.user_profile.language = lang
            self.user_profile.save()
            
            response = self.client.get('/add_viewing/')
            self.assertEqual(response.status_code, 200)
            
            # Vérifier que la page contient des traductions
            if lang == 'fr':
                self.assertContains(response, 'Étape 1')
            elif lang == 'de':
                self.assertContains(response, 'Schritt 1')
            elif lang == 'es':
                self.assertContains(response, 'Paso 1')
    
    def tearDown(self):
        """Nettoyage après les tests"""
        # Supprimer tous les visionnages et films créés pendant les tests
        Viewing.objects.filter(user=self.user).delete()
        Movie.objects.filter(original_title__in=['Test Movie', 'Interstellar']).delete()
        self.user.delete()
        self.user_profile.delete()


if __name__ == '__main__':
    import unittest
    unittest.main()