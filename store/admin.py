from django.contrib import admin
from .models import Movie, MovieTranslation, TMDBApiLog


class MovieTranslationInline(admin.TabularInline):
    model = MovieTranslation
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('original_title', 'year', 'director', 'original_language', 'tmdb_id', 'has_poster')
    search_fields = ('original_title', 'director')
    inlines = [MovieTranslationInline]

    @admin.display(boolean=True, description='Poster')
    def has_poster(self, obj):
        return bool(obj.poster_data)


@admin.register(TMDBApiLog)
class TMDBApiLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'http_method', 'url', 'status_code')
    list_filter = ('http_method', 'status_code', 'timestamp')
    search_fields = ('url',)
    readonly_fields = ('url', 'timestamp', 'http_method', 'status_code', 'response')
    ordering = ('-timestamp',)
