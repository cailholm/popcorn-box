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

def test_home_styles():
    """Test des styles de la page d'accueil"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST: STYLES DE LA PAGE D'ACCUEIL")
    print("=" * 60)
    
    # Test 1: Vérifier que la page se charge correctement
    print("\n1. Chargement de la page d'accueil")
    response = client.get('/')
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Page chargée avec succès")
    else:
        print("✗ Problème de chargement de la page")
        return
    
    # Test 2: Vérifier la présence des éléments principaux
    print("\n2. Éléments principaux de la page")
    content = response.content.decode('utf-8')
    
    elements = [
        ('welcome-description', 'Description de bienvenue'),
        ('features-list', 'Liste des fonctionnalités'),
        ('get-started-section', 'Section démarrer'),
        ('popular-movies-title', 'Titre films populaires'),
        ('popular-movies-grid', 'Grille films populaires')
    ]
    
    for element_class, description in elements:
        if f'class="{element_class}"' in content:
            print(f"✓ {description} présente")
        else:
            print(f"✗ {description} absente")
    
    # Test 3: Vérifier la présence des styles
    print("\n3. Styles CSS")
    
    style_blocks = [
        ('welcome-description', '.welcome-description'),
        ('features-list', '.features-list'),
        ('popular-movies-grid', '.popular-movies-grid'),
        ('popular-movie-card', '.popular-movie-card')
    ]
    
    for element_class, style_selector in style_blocks:
        if style_selector in content:
            print(f"✓ Style pour {element_class} présent")
        else:
            print(f"✗ Style pour {element_class} absent")
    
    # Test 4: Vérifier les variables CSS
    print("\n4. Variables CSS")
    
    css_vars = [
        ('--popcorn-red', 'Couleur rouge popcorn'),
        ('--popcorn-gold', 'Couleur or popcorn'),
        ('--border-radius', 'Border radius'),
        ('--box-shadow', 'Box shadow')
    ]
    
    for var_name, description in css_vars:
        if var_name in content:
            print(f"✓ Variable {var_name} présente")
        else:
            print(f"✗ Variable {var_name} absente")
    
    # Test 5: Vérifier la structure du bloc extra_css
    print("\n5. Structure du bloc extra_css")
    
    if '{% block extra_css %}' in content and '{% endblock %}' in content:
        print("✓ Bloc extra_css présent")
        
        # Extraire le contenu du bloc extra_css
        extra_css_start = content.find('{% block extra_css %}')
        extra_css_end = content.find('{% endblock %}', extra_css_start)
        extra_css_content = content[extra_css_start:extra_css_end]
        
        if '<style>' in extra_css_content and '</style>' in extra_css_content:
            print("✓ Balises style présentes dans extra_css")
        else:
            print("✗ Balises style absentes dans extra_css")
            
        # Vérifier la taille du contenu CSS
        if len(extra_css_content) > 1000:  # Plus de 1000 caractères
            print(f"✓ Contenu CSS substantiel ({len(extra_css_content)} caractères)")
        else:
            print(f"⚠️  Contenu CSS court ({len(extra_css_content)} caractères)")
    else:
        print("✗ Bloc extra_css absent")
    
    # Test 6: Vérifier les fichiers CSS statiques
    print("\n6. Fichiers CSS statiques")
    
    if 'popcorn-theme.css' in content:
        print("✓ Fichier popcorn-theme.css référencé")
    else:
        print("✗ Fichier popcorn-theme.css non référencé")
    
    if 'font-awesome' in content:
        print("✓ Font Awesome référencé")
    else:
        print("✗ Font Awesome non référencé")
    
    print("\n" + "=" * 60)
    print("ANALYSE TERMINÉE")
    print("=" * 60)
    
    print("\nRecommandations:")
    print("- Vérifier que les classes CSS dans le HTML correspondent aux sélecteurs CSS")
    print("- Vérifier que les styles inline dans extra_css sont correctement formatés")
    print("- Vérifier qu'il n'y a pas de conflits de spécificité CSS")
    print("- Vérifier que les fichiers CSS statiques sont accessibles")

if __name__ == '__main__':
    test_home_styles()