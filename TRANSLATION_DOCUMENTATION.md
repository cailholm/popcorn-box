# Documentation de la fonctionnalité de traduction

## Aperçu

La fonctionnalité de traduction permet de récupérer automatiquement les traductions des titres et résumés de films depuis l'API The Movie Database (TMDb).

## Utilisation

### Méthode `translate()` du Manager MovieTranslation

La méthode `translate()` est disponible via le manager `MovieTranslation.objects` et permet de récupérer ou créer une traduction pour un film dans une langue spécifique.

**Signature :**
```python
MovieTranslation.objects.translate(movie, language_code)
```

**Paramètres :**
- `movie` : Instance du modèle `Movie` pour lequel vous souhaitez obtenir une traduction
- `language_code` : Code de langue ISO 639-1 (ex: 'fr', 'es', 'de', 'en')

**Retourne :**
- Instance de `MovieTranslation` contenant la traduction

**Comportement :**
1. Vérifie d'abord si la traduction existe déjà dans la base de données
2. Si la traduction n'existe pas, interroge l'API TMDb pour obtenir la traduction
3. Si la traduction est trouvée dans TMDb, crée un nouvel enregistrement dans la base de données
4. Si la traduction n'est pas disponible dans TMDb, crée un enregistrement avec les données originales du film
5. En cas d'erreur avec l'API TMDb, crée un enregistrement avec les données originales du film

## Exemple d'utilisation

```python
from store.models import Movie, MovieTranslation

# Créer ou obtenir un film
movie = Movie.objects.get(original_title="Inception")

# Récupérer ou créer une traduction française
translation_fr = MovieTranslation.objects.translate(movie, 'fr')

print(f"Titre français: {translation_fr.title}")
print(f"Résumé français: {translation_fr.summary}")

# Récupérer ou créer une traduction espagnole
translation_es = MovieTranslation.objects.translate(movie, 'es')

print(f"Titre espagnol: {translation_es.title}")
print(f"Résumé espagnol: {translation_es.summary}")
```

## Langues supportées

Les langues actuellement supportées sont :
- Anglais ('en')
- Français ('fr')
- Allemand ('de')
- Espagnol ('es')

## Gestion des erreurs

La méthode `translate()` est conçue pour être robuste et gérer les erreurs gracieusement :

1. **Erreurs de réseau** : Si l'API TMDb n'est pas disponible, la méthode crée une traduction avec les données originales
2. **Film non trouvé** : Si le film n'est pas trouvé dans TMDb, la méthode crée une traduction avec les données originales
3. **Traduction non disponible** : Si une traduction pour la langue demandée n'est pas disponible, la méthode utilise les données originales

## Intégration avec l'application existante

Cette fonctionnalité peut être intégrée dans les vues existantes pour fournir des traductions automatiques. Par exemple, dans la vue `movie_list`, vous pouvez utiliser :

```python
def movie_list(request):
    # Récupérer la langue de l'utilisateur
    language = get_user_language(request)  # 'fr', 'es', etc.
    
    # Récupérer les films avec leurs traductions
    movies = Movie.objects.all()
    translated_movies = []
    
    for movie in movies:
        translation = MovieTranslation.objects.translate(movie, language)
        translated_movies.append({
            'movie': movie,
            'translated_title': translation.title,
            'translated_summary': translation.summary
        })
    
    return render(request, 'movie_list.html', {'movies': translated_movies})
```

## Notes techniques

- La méthode utilise l'API key TMDb suivante : `0d52b79b3e5cf36801f31ccfda872d54`
- Les traductions sont stockées dans la base de données pour éviter des appels API répétés
- La méthode respecte le principe de "graceful degradation" - elle fournit toujours un résultat même en cas d'échec