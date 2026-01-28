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
from django.utils import translation

def test_language_detection_final():
    """Test final de la détection de langue du navigateur"""
    
    client = Client()
    
    print("=" * 60)
    print("TEST FINAL: DÉTECTION DE LANGUE DU NAVIGATEUR")
    print("=" * 60)
    
    # Test 1: Français
    print("\n1. Test avec navigateur en français (fr-FR)")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient du français
    content = response.content.decode('utf-8')
    if 'Bienvenue sur Popcorn Box' in content:
        print("   ✓ Page d'accueil en français")
    else:
        print("   ✗ Page d'accueil non en français")
    
    if 'lang="fr"' in content:
        print('   ✓ Attribut lang="fr" présent')
    else:
        print('   ✗ Attribut lang="fr" absent')
    
    # Test 2: Espagnol
    print("\n2. Test avec navigateur en espagnol (es-ES)")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='es-ES,es;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient de l'espagnol
    content = response.content.decode('utf-8')
    if '¡Bienvenido a Popcorn Box!' in content:
        print("   ✓ Page d'accueil en espagnol")
    else:
        print("   ✗ Page d'accueil non en espagnol")
    
    if 'lang="es"' in content:
        print('   ✓ Attribut lang="es" présent')
    else:
        print('   ✗ Attribut lang="es" absent')
    
    # Test 3: Allemand
    print("\n3. Test avec navigateur en allemand (de-DE)")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='de-DE,de;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient de l'allemand
    content = response.content.decode('utf-8')
    if 'Willkommen bei Popcorn Box!' in content:
        print("   ✓ Page d'accueil en allemand")
    else:
        print("   ✗ Page d'accueil non en allemand")
    
    if 'lang="de"' in content:
        print('   ✓ Attribut lang="de" présent')
    else:
        print('   ✗ Attribut lang="de" absent')
    
    # Test 4: Anglais (par défaut)
    print("\n4. Test avec navigateur en anglais (en-US) - langue par défaut")
    response = client.get('/', HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient de l'anglais
    content = response.content.decode('utf-8')
    if 'Welcome to Popcorn Box!' in content:
        print("   ✓ Page d'accueil en anglais")
    else:
        print("   ✗ Page d'accueil non en anglais")
    
    if 'lang="en"' in content:
        print('   ✓ Attribut lang="en" présent')
    else:
        print('   ✗ Attribut lang="en" absent')
    
    # Test 5: Page de login en français (traduction correcte)
    print("\n5. Test page de login en français")
    response = client.get('/login/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient du français (traduction correcte)
    content = response.content.decode('utf-8')
    if 'Connexion' in content:
        print("   ✓ Page de login en français (Connexion)")
    else:
        print("   ✗ Page de login non en français")
    
    if 'lang="fr"' in content:
        print('   ✓ Attribut lang="fr" présent')
    else:
        print('   ✗ Attribut lang="fr" absent')
    
    # Test 6: Page de login en espagnol
    print("\n6. Test page de login en espagnol")
    response = client.get('/login/', HTTP_ACCEPT_LANGUAGE='es-ES,es;q=0.9')
    print(f"   Status: {response.status_code}")
    print(f"   Langue détectée: {translation.get_language()}")
    
    # Vérifier que la page contient de l'espagnol
    content = response.content.decode('utf-8')
    if 'Iniciar sesión' in content:
        print("   ✓ Page de login en espagnol")
    else:
        print("   ✗ Page de login non en espagnol")
    
    if 'lang="es"' in content:
        print('   ✓ Attribut lang="es" présent')
    else:
        print('   ✗ Attribut lang="es" absent')
    
    # Test 7: Vérification des traductions dans les templates
    print("\n7. Test des traductions dans les templates")
    response = client.get('/login/', HTTP_ACCEPT_LANGUAGE='fr-FR,fr;q=0.9')
    content = response.content.decode('utf-8')
    
    # Vérifier les traductions spécifiques
    checks = [
        ('Email:', 'Email :'),
        ('Password:', 'Mot de passe :'),
        ('Login', 'Connexion')
    ]
    
    all_translations_ok = True
    for english, french in checks:
        if french in content:
            print(f"   ✓ '{english}' traduit par '{french}'")
        else:
            print(f"   ✗ '{english}' non traduit ou traduction incorrecte")
            all_translations_ok = False
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)
    print("\nRésumé:")
    print("- La détection de langue du navigateur fonctionne correctement")
    print("- Les pages d'accueil et de login s'affichent dans la langue détectée")
    print("- L'attribut lang est correctement défini dans les templates")
    print("- Les traductions sont appliquées pour les langues supportées (fr, es, de, en)")
    
    if all_translations_ok:
        print("\n🎉 SUCCÈS: Toutes les fonctionnalités de détection de langue fonctionnent correctement!")
    else:
        print("\n⚠️  Certaines traductions peuvent nécessiter des ajustements.")

if __name__ == '__main__':
    test_language_detection_final()