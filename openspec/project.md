# Project Context

## Purpose
The Popcorn Box project is a web application designed to allow users to track and rate movies they have watched. Users can search for movies using an external API (The Movie Database - TMDb), add them to their personal list, and assign ratings. The application also provides a login system for user authentication and personalized movie tracking.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (with Django templates)
- **Database**: SQLite (default Django database)
- **External API**: The Movie Database (TMDb) API
- **Authentication**: Django's built-in authentication system
- **Dependencies**: `requests` library for API calls

## Project Conventions

### Code Style
- **Python**: Follows PEP 8 guidelines
- **Django**: Follows Django best practices and conventions
- **Naming Conventions**:
  - Models: PascalCase (e.g., `Movie`, `Viewing`)
  - Views: snake_case (e.g., `login_view`, `movie_list`)
  - Templates: snake_case (e.g., `login.html`, `movie_list.html`)
  - URLs: snake_case (e.g., `login/`, `movies/`)

### Architecture Patterns
- **MVC Pattern**: Django's built-in Model-View-Template (MVT) architecture
- **Separation of Concerns**: Clear separation between models, views, and templates
- **Reusable Components**: Common templates and static files for consistent UI

### Testing Strategy
- **Manual Testing**: Primary testing method for now
- **Future Testing**: Plan to implement unit tests and integration tests using Django's testing framework

### Git Workflow
- **Branching Strategy**: Simple branching with `main` as the primary branch
- **Commit Conventions**: Descriptive commit messages explaining changes
- **Pull Requests**: Used for reviewing and merging significant changes

## Domain Context
- **Movie Tracking**: Users can track movies they have watched
- **Rating System**: Users can rate movies on a scale of 0 to 5 (with 0.5 increments)
- **User Authentication**: Users must log in to access their movie list and add new viewings

## Important Constraints
- **API Rate Limits**: TMDb API has rate limits that need to be respected
- **Data Privacy**: User data and movie ratings are stored locally and should be handled with care
- **Performance**: API calls to TMDb should be optimized to minimize latency

## External Dependencies
- **The Movie Database (TMDb) API**: Used to search for movies and retrieve movie details
- **Django**: Web framework for building the application
- **SQLite**: Default database for Django, used for storing user data and movie information
- **requests Library**: Used for making HTTP requests to the TMDb API
