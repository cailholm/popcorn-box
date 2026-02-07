# Views package initialization
# This file will import and expose all views from submodules

from .auth_views import login_view, logout_view, signup_view
from .movie_views import movie_list, movie_detail, search_movies_api
from .viewing_views import add_viewing, my_viewings
from .profile_views import profile, home