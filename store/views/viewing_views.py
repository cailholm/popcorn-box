from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from ..models import Movie, Viewing, UserProfile
from ..helpers import TMDBClient
import requests

@login_required
def add_viewing(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        
        try:
            movie = Movie.objects.get(pk=movie_id)
            
            # Créer un nouveau visionnage
            viewing = Viewing.objects.create(
                user=request.user,
                movie=movie,
                rating=rating if rating else None,
                review=review,
                date_watched=timezone.now()
            )
            
            messages.success(request, _('Viewing added successfully!'))
            return redirect('my_viewings')
            
        except Movie.DoesNotExist:
            messages.error(request, _('Movie not found.'))
            return redirect('movie_list')
    
    # Si ce n'est pas une requête POST, rediriger vers la liste des films
    return redirect('movie_list')

@login_required
def my_viewings(request):
    # Récupérer tous les visionnages de l'utilisateur
    viewings = Viewing.objects.filter(user=request.user).order_by('-date_watched')
    
    # Récupérer la langue de l'utilisateur
    language = 'en'  # Langue par défaut
    try:
        user_profile = request.user.userprofile
        language = user_profile.language if user_profile.language else 'en'
    except:
        pass
    
    # Grouper les visionnages par date
    viewings_by_date = {}
    for viewing in viewings:
        date_str = viewing.date_watched.strftime('%Y-%m-%d')
        if date_str not in viewings_by_date:
            viewings_by_date[date_str] = []
        
        # Essayer de récupérer la traduction du film
        try:
            translation = viewing.movie.movietranslation_set.get(language=language)
            viewing.movie.title = translation.title
        except:
            pass  # Garder le titre original
        
        viewings_by_date[date_str].append(viewing)
    
    return render(request, 'my_viewings.html', {
        'viewings_by_date': viewings_by_date,
        'title': _('My Viewings')
    })