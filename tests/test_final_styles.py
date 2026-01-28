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

def test_final_styles():
    """Test final des styles de la page d'accueil"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST FINAL: STYLES DE LA PAGE D'ACCUEIL")
    print("=" * 60)
    
    # Test 1: Vérifier que la page se charge correctement
    print("\n1. Chargement de la page d'accueil")
    response = client.get('/')
    content = response.content.decode('utf-8')
    
    if response.status_code == 200:
        print("✓ Page chargée avec succès")
    else:
        print("✗ Problème de chargement de la page")
        return
    
    # Test 2: Vérifier les styles critiques
    print("\n2. Styles critiques")
    
    critical_styles = [
        ('.welcome-description', 'Style pour la description de bienvenue'),
        ('.features-list', 'Style pour la liste des fonctionnalités'),
        ('.popular-movies-grid', 'Style pour la grille de films'),
        ('.popular-movie-card', 'Style pour les cartes de films'),
        ('.get-started-section', 'Style pour la section démarrer')
    ]
    
    all_styles_present = True
    for style_selector, description in critical_styles:
        if style_selector in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            all_styles_present = False
    
    # Test 3: Vérifier les variables CSS
    print("\n3. Variables CSS")
    
    css_vars = [
        ('--popcorn-red: #d62828', 'Couleur rouge popcorn'),
        ('--popcorn-gold: #ffb300', 'Couleur or popcorn'),
        ('--border-radius: 8px', 'Border radius'),
        ('--box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)', 'Box shadow')
    ]
    
    all_vars_present = True
    for var_def, description in css_vars:
        if var_def in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            all_vars_present = False
    
    # Test 4: Vérifier les media queries
    print("\n4. Media queries (responsive)")
    
    media_queries = [
        ('@media (max-width: 768px)', 'Media query pour tablettes'),
        ('@media (max-width: 480px)', 'Media query pour mobiles')
    ]
    
    all_media_present = True
    for media_query, description in media_queries:
        if media_query in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            all_media_present = False
    
    # Test 5: Vérifier les styles spécifiques
    print("\n5. Styles spécifiques")
    
    specific_styles = [
        ('font-size: 1.1rem', 'Taille de police pour description'),
        ('grid-template-columns:', 'Grille CSS'),
        ('display: flex', 'Affichage flex'),
        ('justify-content:', 'Alignement flex')
    ]
    
    all_specific_present = True
    for style_property, description in specific_styles:
        if style_property in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            all_specific_present = False
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    if all_styles_present and all_vars_present and all_media_present and all_specific_present:
        print("\n🎉 SUCCÈS: Tous les styles sont correctement chargés!")
        print("\nLa page d'accueil devrait maintenant s'afficher avec:")
        print("- Les bons styles pour tous les éléments")
        print("- Les couleurs du thème popcorn")
        print("- Les styles responsive pour mobiles et tablettes")
        print("- Les animations et effets visuels")
    else:
        print("\n⚠️  Certains styles peuvent être manquants.")
        print("Vérifiez les éléments suivants:")
        if not all_styles_present:
            print("- Certains styles critiques sont manquants")
        if not all_vars_present:
            print("- Certaines variables CSS sont manquantes")
        if not all_media_present:
            print("- Certaines media queries sont manquantes")
        if not all_specific_present:
            print("- Certains styles spécifiques sont manquants")

if __name__ == '__main__':
    test_final_styles()