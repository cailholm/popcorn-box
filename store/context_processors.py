from django.utils import translation

def language_context(request):
    """
    Contexte processeur pour ajouter la langue actuelle au contexte des templates.
    """
    return {
        'LANGUAGE_CODE': translation.get_language(),
    }