from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from ..models import UserProfile

def home(request):
    if request.user.is_authenticated:
        # Récupérer la langue de l'utilisateur
        language = 'en'  # Langue par défaut
        try:
            user_profile = request.user.userprofile
            language = user_profile.language if user_profile.language else 'en'
        except:
            pass
        
        return render(request, 'home.html', {
            'title': _('Home'),
            'user_language': language
        })
    else:
        return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        # Mettre à jour les informations du profil
        language = request.POST.get('language')
        
        try:
            user_profile = request.user.userprofile
            user_profile.language = language
            user_profile.save()
            
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
        except UserProfile.DoesNotExist:
            # Créer un profil si inexistant
            user_profile = UserProfile.objects.create(
                user=request.user,
                language=language
            )
            messages.success(request, _('Profile created successfully!'))
            return redirect('profile')
    
    # Récupérer les informations actuelles du profil
    try:
        user_profile = request.user.userprofile
        current_language = user_profile.language if user_profile.language else 'en'
    except UserProfile.DoesNotExist:
        current_language = 'en'
    
    return render(request, 'profile.html', {
        'title': _('Profile'),
        'current_language': current_language
    })