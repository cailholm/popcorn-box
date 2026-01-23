from django.urls import path
from .views import login_view, movie_list, logout_view, add_viewing, my_viewings, profile, movie_detail, search_movies_api

urlpatterns = [
    path('login/', login_view, name='login'),
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('logout/', logout_view, name='logout'),
    path('add_viewing/', add_viewing, name='add_viewing'),
    path('my_viewings/', my_viewings, name='my_viewings'),
    path('profile/', profile, name='profile'),
    # API endpoint pour la recherche AJAX
    path('api/search-movies/', search_movies_api, name='search_movies_api'),
]