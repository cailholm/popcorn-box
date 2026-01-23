# Popcorn Box 🍿

**Popcorn Box** is a Django web application that allows users to track and rate movies they have watched. Users can search for movies using the TMDb (The Movie Database) API, add them to their personal list, and assign ratings.

## 🎬 Features

- **Movie Search**: Search for movies via the TMDb API
- **Viewing Tracking**: Add movies to your personal list with date and rating
- **Rating System**: Rate movies from 0 to 5 stars (in 0.5 increments)
- **Multilingual**: Interface available in English, French, Spanish, and German
- **Authentication**: Secure login system
- **User Profiles**: Customize preferred language
- **Poster Display**: View movie posters

## 📸 Screenshots

*(To be added: screenshots of the application in action)*

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- GitHub account (for optional deployment)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/popcorn-box.git
   cd popcorn-box
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with the following content:
   ```env
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   TMDB_API_KEY=your_tmdb_api_key
   ```
   
   > **Note**: Get a free TMDb API key at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

5. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Compile translations**:
   ```bash
   python manage.py compilemessages
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   Open your browser to [http://localhost:8000](http://localhost:8000)

## 🌍 Multilingual Configuration

The application supports 4 languages:

- **English** (en) - Default language
- **French** (fr)
- **Spanish** (es)
- **German** (de)

### Adding a New Language

1. Create translation files:
   ```bash
   python manage.py makemessages -l xx  # Replace xx with language code
   ```

2. Translate strings in `locale/xx/LC_MESSAGES/django.po`

3. Compile translations:
   ```bash
   python manage.py compilemessages
   ```

## 🔧 Configuration

### Important Files

- `popcorn_box/settings.py` - Main Django configuration
- `store/helpers.py` - TMDb API client configuration
- `store/middleware.py` - Language handling middleware
- `.env` - Environment variables (do not commit)

### TMDb API Settings

Modify TMDb API settings in `store/helpers.py`:

```python
class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = os.getenv('TMDB_API_KEY', 'your_default_key')
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
```

## 📂 Project Structure

```
popcorn_box/
├── popcorn_box/                  # Django configuration
│   ├── settings.py              # Application settings
│   ├── urls.py                  # Main routing
│   └── wsgi.py                  # WSGI configuration
│
├── store/                       # Main application
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── movie_list.html      # Movie list
│   │   ├── my_viewings.html      # My viewings
│   │   ├── add_viewing.html      # Add viewing
│   │   ├── profile.html         # User profile
│   │   └── login.html           # Login page
│   │
│   ├── static/                 # Static files
│   │   └── js/                  # JavaScript
│   │       └── movie_search.js  # Movie search
│   │
│   ├── models.py               # Data models
│   ├── views.py                 # View logic
│   ├── helpers.py               # TMDb client
│   ├── middleware.py            # Language middleware
│   ├── admin.py                 # Admin configuration
│   └── urls.py                  # Application routing
│
├── locale/                      # Translation files
│   ├── fr/                      # French
│   ├── es/                      # Spanish
│   ├── de/                      # German
│   └── en/                      # English
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                     # This file
```

## 🎥 Data Models

### Movie
- `tmdb_id`: TMDb identifier
- `original_title`: Original title
- `release_date`: Release date
- `overview`: Summary
- `poster_path`: Path to poster
- `poster_data`: Binary poster data

### Viewing
- `user`: User
- `movie`: Movie
- `date_viewed`: Viewing date
- `rating`: Rating (0-5)

### UserProfile
- `user`: User
- `language`: Preferred language

### MovieTranslation
- `movie`: Movie
- `language`: Language
- `translated_title`: Translated title
- `is_fallback`: Indicates if it's a fallback translation

## 🔌 TMDb API

The application uses the TMDb API for:

- Searching movies by title
- Retrieving movie details
- Getting movie posters

### Search Example

```python
from store.helpers import TMDBClient

client = TMDBClient()
results = client.search_movies("Inception")
for movie in results:
    print(f"{movie['title']} ({movie['release_date']})")
```

## 🧪 Tests

The application includes various tests to ensure proper functionality:

- **Unit tests**: Model and view tests
- **Integration tests**: Complete workflow tests
- **Translation tests**: Multilingual verification
- **JavaScript tests**: Search functionality tests

### Running Tests

```bash
# Run all tests
python manage.py test

# Run a specific test
python test_final_integration.py

# Run translation tests
python test_final_translation.py
```

## 🛠 Deployment

### Deployment on Heroku

1. Install Heroku CLI
2. Create a new Heroku project
3. Add necessary buildpacks
4. Deploy with:
   ```bash
   git push heroku master
   ```

### Deployment on a Server

1. Set up a server with Nginx and Gunicorn
2. Install system dependencies
3. Configure environment variables
4. Launch with Gunicorn:
   ```bash
   gunicorn popcorn_box.wsgi:application --bind 0.0.0.0:8000
   ```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Support

For any questions or issues, please open an issue on GitHub.

## 🎉 Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework
- [TMDb](https://www.themoviedb.org/) - Movie database
- [Bootstrap](https://getbootstrap.com/) - CSS framework (optional)

---

**Popcorn Box** © 2024 - A movie tracking application for film enthusiasts 🎥