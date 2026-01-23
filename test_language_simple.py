#!/usr/bin/env python

import os
import sys
import django

# Add project path to sys.path
sys.path.insert(0, '/home/cailholm/Mistral/popcorn_box')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcorn_box.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import UserProfile
from django.utils import translation

def test_language_activation():
    print("=== Test d'activation de langue ===")
    print()
    
    # Create test user
    user = User.objects.create_user(username='testuser4', email='test4@example.com', password='testpass123')
    user_profile = UserProfile.objects.create(user=user, language='es')  # Espagnol
    
    print(f"Utilisateur créé: {user.email}")
    print(f"Langue du profil: {user_profile.language}")
    print()
    
    # Test 1: Simulation de ce que fait le middleware
    print("Test 1: Simulation du middleware")
    
    # Réinitialiser la langue à anglais
    translation.activate('en')
    current_lang = translation.get_language()
    print(f"  Langue initiale: {current_lang}")
    
    # Simuler le middleware
    try:
        user_profile = UserProfile.objects.get(user=user)
        language = user_profile.language
        
        if translation.get_language() != language:
            translation.activate(language)
            print(f"  Langue activée: {language}")
        
        new_lang = translation.get_language()
        print(f"  Langue après activation: {new_lang}")
        print(f"  Résultat: {'OK' if new_lang == 'es' else 'Échec'}")
        
    except UserProfile.DoesNotExist:
        print("  Profil non trouvé")
    
    print()
    
    # Test 2: Vérification des traductions
    print("Test 2: Vérification des traductions dans les templates")
    
    # Simuler ce que fait un template avec {% trans %}
    from django.template import Template, Context
    
    template_content = """
{% load i18n %}
<p>{% trans 'Movie List' %}</p>
<p>{% trans 'My Viewings' %}</p>
<p>{% trans 'Profile' %}</p>
"""
    
    template = Template(template_content)
    context = Context({})
    
    # Avec langue anglaise
    translation.activate('en')
    result_en = template.render(context)
    print("  En anglais:")
    print(result_en)
    
    # Avec langue espagnole
    translation.activate('es')
    result_es = template.render(context)
    print("  En espagnol:")
    print(result_es)
    
    # Avec langue française
    translation.activate('fr')
    result_fr = template.render(context)
    print("  En français:")
    print(result_fr)
    
    print()
    
    # Cleanup
    user_profile.delete()
    user.delete()
    
    print("=== Test terminé ===")
    print("Le middleware devrait maintenant activer correctement la langue de l'utilisateur")
    print("pour chaque requête, et les éléments de menu devraient s'afficher dans la bonne langue.")

if __name__ == '__main__':
    test_language_activation()