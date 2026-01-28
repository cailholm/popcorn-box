from django.utils import translation
from django.contrib.auth.models import User
from .models import UserProfile

class UserLanguageMiddleware:
    """
    Middleware pour activer automatiquement la langue de l'utilisateur
    à partir de son profil pour chaque requête.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Vérifier si l'utilisateur est authentifié et a un ID (est sauvegardé en base)
        if hasattr(request, 'user') and request.user.is_authenticated and hasattr(request.user, 'id') and request.user.id:
            try:
                # Récupérer le profil de l'utilisateur
                user_profile = UserProfile.objects.get(user=request.user)
                language = user_profile.language
                
                # Activer la langue si elle est différente de la langue actuelle
                if translation.get_language() != language:
                    translation.activate(language)
                    if hasattr(request, 'session'):
                        request.session['_language'] = language
                    
            except UserProfile.DoesNotExist:
                # Si le profil n'existe pas, utiliser la langue par défaut
                pass
        else:
            # Pour les utilisateurs non authentifiés, s'assurer que la langue du navigateur
            # est utilisée (LocaleMiddleware devrait déjà l'avoir définie)
            # Nous pouvons vérifier si une langue a été définie par LocaleMiddleware
            current_language = translation.get_language()
            if current_language and hasattr(request, 'session'):
                # S'assurer que la langue est sauvegardée dans la session
                request.session['_language'] = current_language
        
        response = self.get_response(request)
        return response