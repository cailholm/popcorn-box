from django.urls import path
from .views.movie_views import refresh_movie_from_tmdb
from .views.auth_views import login_view, signup_view, logout_view
from .views.movie_views import movie_list, movie_detail
from .views.viewing_views import add_viewing, my_viewings
from .views.profile_views import profile, home
from .views.movie_views import search_movies_api

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('logout/', logout_view, name='logout'),
    path('add_viewing/', add_viewing, name='add_viewing'),
    path('my_viewings/', my_viewings, name='my_viewings'),
    path('profile/', profile, name='profile'),
    # API endpoint pour la recherche AJAX
    path('api/search-movies/', search_movies_api, name='search_movies_api'),
    # Rafraîchir les informations d'un film depuis TMDB
    path('refresh_movie/<int:movie_id>/', refresh_movie_from_tmdb, name='refresh_movie'),
]