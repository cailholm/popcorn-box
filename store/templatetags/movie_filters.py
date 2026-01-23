from django import template
from ..models import MovieTranslation

register = template.Library()

@register.simple_tag(name='get_movie_translation')
def get_movie_translation(movie, language):
    try:
        return MovieTranslation.objects.get(movie=movie, language=language)
    except MovieTranslation.DoesNotExist:
        return None