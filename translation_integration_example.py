#!/usr/bin/env python
"""
Exemple d'intégration de la fonctionnalité de traduction dans les vues Django.

Ce fichier montre comment vous pouvez intégrer la méthode translate()
dans vos vues existantes pour fournir des traductions automatiques.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Movie, MovieTranslation, UserProfile

def get_user_language(request):
    """
    Helper function to get the user's preferred language.
    """
    language = 'en'  # Default language
    try:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            language = user_profile.language
    except UserProfile.DoesNotExist:
        pass
    return language

@login_required
def movie_list_with_translations(request):
    """
    Example of how to integrate translations in the movie_list view.
    """
    # Get user's preferred language
    language = get_user_language(request)
    
    # Get all movies
    movies = Movie.objects.all()
    
    # Create a list to store movies with their translations
    translated_movies = []
    
    for movie in movies:
        # Get or create translation for this movie
        translation = MovieTranslation.objects.translate(movie, language)
        
        translated_movies.append({
            'movie': movie,
            'title': translation.title,
            'summary': translation.summary,
            'year': movie.year,
            'director': movie.director,
            'original_title': movie.original_title,  # Keep original for reference
            'language': language
        })
    
    return render(request, 'movie_list.html', {
        'movies': translated_movies,
        'language': language,
        'title': 'Movie List'
    })

@login_required
def movie_detail_with_translation(request, movie_id):
    """
    Example of a movie detail view with translation support.
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        language = get_user_language(request)
        
        # Get or create translation
        translation = MovieTranslation.objects.translate(movie, language)
        
        return render(request, 'movie_detail.html', {
            'movie': movie,
            'translated_title': translation.title,
            'translated_summary': translation.summary,
            'language': language,
            'title': translation.title
        })
        
    except Movie.DoesNotExist:
        return redirect('movie_list')

def add_viewing_with_translation(request):
    """
    Example of how to integrate translations when adding a new viewing.
    This shows how to automatically create translations when a new movie is added.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        date = request.POST.get('date')
        rating = request.POST.get('rating')
        
        # ... existing code to find or create movie ...
        
        # After creating the movie, automatically create translations for all supported languages
        if movie:
            # Create translations for all supported languages
            for lang_code, lang_name in MovieTranslation.LANGUAGE_CHOICES:
                MovieTranslation.objects.translate(movie, lang_code)
            
            # ... rest of the existing code ...

# Example of how to use in templates:
"""
{% for movie in movies %}
    <div class="movie-card">
        <h3>{{ movie.title }}</h3>  <!-- This will show the translated title -->
        <p><strong>Original title:</strong> {{ movie.original_title }}</p>
        <p><strong>Year:</strong> {{ movie.year }}</p>
        <p><strong>Director:</strong> {{ movie.director }}</p>
        <p>{{ movie.summary }}</p>  <!-- This will show the translated summary -->
        
        {% if movie.language != 'en' %}
            <small>Translated from English to {{ movie.language }}</small>
        {% endif %}
    </div>
{% endfor %}
"""

# Example of language switcher in template:
"""
<div class="language-switcher">
    <form method="post" action="{% url 'update_language' %}">
        {% csrf_token %}
        <select name="language">
            <option value="en" {% if language == 'en' %}selected{% endif %}>English</option>
            <option value="fr" {% if language == 'fr' %}selected{% endif %}>Français</option>
            <option value="es" {% if language == 'es' %}selected{% endif %}>Español</option>
            <option value="de" {% if language == 'de' %}selected{% endif %}>Deutsch</option>
        </select>
        <button type="submit">Change Language</button>
    </form>
</div>
"""

if __name__ == '__main__':
    print("This file contains examples of how to integrate the translation functionality.")
    print("Copy the relevant functions to your views.py file and adapt as needed.")