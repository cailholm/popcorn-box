// Movie Search JavaScript - Separate file for better organization
// This handles the two-step movie search and selection process

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const searchButton = document.getElementById('search-movie-btn');
    const searchInput = document.getElementById('search_movie_title');
    const searchResults = document.getElementById('search-results');
    const resultsList = document.getElementById('movie-results-list');
    const viewingFormContainer = document.getElementById('viewing-form-container');
    const selectedMovieTitle = document.getElementById('movie_title_display');
    const selectedMovieId = document.getElementById('selected_movie_id');
    const selectedMovieTitleInput = document.getElementById('selected_movie_title');
    
    // Messages will be set from Django template
    // Using English keys only, translations handled by Django
    const messages = {
        minChars: window.movieSearchMessages?.minChars || 'Please enter at least 2 characters',
        searching: window.movieSearchMessages?.searching || 'Searching...',
        noResults: window.movieSearchMessages?.noResults || 'No movies found. Try a different search.',
        error: window.movieSearchMessages?.error || 'An error occurred while searching for movies.',
        noDescription: window.movieSearchMessages?.noDescription || 'No description available'
    };
    
    // Search function - make it globally accessible
    window.searchMovies = function(page = 1) {
        const query = searchInput.value.trim();
        
        if (query.length < 2) {
            alert(messages.minChars);
            return;
        }
        
        // Show loading state
        resultsList.innerHTML = '<p>' + messages.searching + '</p>';
        searchResults.style.display = 'block';
        
        // AJAX request to search movies with pagination
        fetch(`/api/search-movies/?query=${encodeURIComponent(query)}&page=${page}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.movies.length === 0) {
                    resultsList.innerHTML = '<p>' + messages.noResults + '</p>';
                } else {
                    // Display results with posters
                    let html = '<ul style="list-style: none; padding: 0;">';
                    data.movies.forEach(movie => {
                        const description = movie.overview || messages.noDescription;
                        
                        // Build poster URL with fallback if config not available
                        const baseUrl = window.tmdbConfig?.imageBaseUrl || 'https://image.tmdb.org/t/p/';
                        const posterSize = window.tmdbConfig?.posterSize || 'w185';
                        const posterUrl = movie.poster_path ? baseUrl + posterSize + movie.poster_path : null;
                        
                        html += `
                            <li style="padding: 10px; border: 1px solid #ddd; margin-bottom: 8px; cursor: pointer; display: flex; align-items: flex-start;"
                                data-movie-id="${movie.id}"
                                data-movie-title="${movie.title}"
                                data-movie-year="${movie.year}">
                                ${posterUrl ? `<img src="${posterUrl}" alt="${movie.title}" style="width: 60px; height: auto; margin-right: 15px; border-radius: 4px;">` : '<div style="width: 60px; height: 90px; background: #ddd; margin-right: 15px; border-radius: 4px; display: flex; align-items: center; justify-content: center;">🎬</div>'}
                                <div style="flex: 1;">
                                    <strong>${movie.title}</strong> (${movie.year})<br>
                                    <small style="display: block; margin-top: 5px; color: #666;">${description}</small>
                                </div>
                            </li>
                        `;
                    });
                    html += '</ul>';
                    
                    // Add pagination controls
                    const pagination = data.pagination;
                    if (pagination.total_pages > 1) {
                        html += '<div style="margin-top: 15px; text-align: center;">';
                        
                        // Previous page button
                        if (pagination.page > 1) {
                            html += `<button data-page="${pagination.page - 1}" class="pagination-btn" style="margin-right: 10px; padding: 5px 10px;">
                                ← ${messages.previous || 'Previous'}
                            </button>`;
                        }
                        
                        // Page info
                        html += `<span style="margin: 0 10px;">
                            ${messages.page || 'Page'} ${pagination.page} ${messages.of || 'of'} ${pagination.total_pages}
                        </span>`;
                        
                        // Next page button
                        if (pagination.page < pagination.total_pages) {
                            html += `<button data-page="${pagination.page + 1}" class="pagination-btn" style="margin-left: 10px; padding: 5px 10px;">
                                ${messages.next || 'Next'} →
                            </button>`;
                        }
                        
                        html += '</div>';
                    }
                    
                    resultsList.innerHTML = html;
                    
                    // Add click handlers for selection
                    addSelectionHandlers();
                    
                    // Add click handlers for pagination
                    addPaginationHandlers();
                }
            })
            .catch(error => {
                console.error('Search error:', error);
                resultsList.innerHTML = '<p>' + messages.error + '</p>';
            });
    }
    
    // Add click handlers to movie results
    function addSelectionHandlers() {
        document.querySelectorAll('#movie-results-list li').forEach(li => {
            li.addEventListener('click', function() {
                const movieId = this.getAttribute('data-movie-id');
                const movieTitle = this.getAttribute('data-movie-title');
                const movieYear = this.getAttribute('data-movie-year');
                
                // Fill the form with selected movie
                selectedMovieTitle.value = movieTitle + ' (' + movieYear + ')';
                selectedMovieId.value = movieId;
                selectedMovieTitleInput.value = movieTitle;
                
                // Hide search and show form
                searchResults.style.display = 'none';
                viewingFormContainer.style.display = 'block';
                
                // Scroll to form
                viewingFormContainer.scrollIntoView({ behavior: 'smooth' });
            });
        });
    }
    
    // Add click handlers to pagination buttons
    function addPaginationHandlers() {
        document.querySelectorAll('.pagination-btn').forEach(button => {
            button.addEventListener('click', function() {
                const page = this.getAttribute('data-page');
                window.searchMovies(parseInt(page));
            });
        });
    }
    
    // Event listeners
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            window.searchMovies(1);
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                window.searchMovies(1);
            }
        });
    }
    
    // Initialize messages from Django if available
    if (window.initMovieSearchMessages) {
        window.initMovieSearchMessages(messages);
    }
});