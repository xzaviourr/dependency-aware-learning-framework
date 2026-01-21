"""
Database layer for the movie recommendation system.
Students will implement SQLite database operations.
"""
import sqlite3
from typing import Tuple, List, Dict, Optional
from framework.decorators import module


@module(dependencies=[], difficulty="easy")
def create_database_connection() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Create a connection to SQLite database.
    
    Database file: movie_recommendations.db
    
    Returns:
        Tuple[connection, cursor]: Database connection and cursor objects
        
    Hint: Use sqlite3.connect('movie_recommendations.db')
    Hint: Set row_factory to sqlite3.Row for dict-like access
    """
    raise NotImplementedError("Students need to implement database connection")


@module(dependencies=["create_database_connection"], difficulty="easy")
def create_users_table() -> None:
    """
    Create the users table in the database.
    
    Schema:
    - user_id: INTEGER PRIMARY KEY AUTOINCREMENT
    - username: TEXT UNIQUE NOT NULL
    - email: TEXT UNIQUE NOT NULL
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    raise NotImplementedError("Students need to implement users table creation")


@module(dependencies=["create_database_connection"], difficulty="easy")
def create_movies_table() -> None:
    """
    Create the movies table in the database.
    
    Schema:
    - movie_id: INTEGER PRIMARY KEY
    - title: TEXT NOT NULL
    - genres: TEXT
    - release_year: INTEGER
    - average_rating: REAL DEFAULT 0.0
    - rating_count: INTEGER DEFAULT 0
    """
    raise NotImplementedError("Students need to implement movies table creation")


@module(dependencies=["create_users_table", "create_movies_table"], difficulty="medium")
def create_ratings_table() -> None:
    """
    Create the ratings table in the database.
    
    Schema:
    - rating_id: INTEGER PRIMARY KEY AUTOINCREMENT
    - user_id: INTEGER REFERENCES users(user_id) ON DELETE CASCADE
    - movie_id: INTEGER REFERENCES movies(movie_id) ON DELETE CASCADE
    - rating: REAL NOT NULL CHECK (rating >= 0.5 AND rating <= 5.0)
    - timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    - UNIQUE(user_id, movie_id)
    
    Hint: Enable foreign keys with: PRAGMA foreign_keys = ON;
    """
    raise NotImplementedError("Students need to implement ratings table creation")


@module(dependencies=["create_users_table"], difficulty="easy")
def insert_user(username: str, email: str) -> int:
    """
    Insert a new user into the database.
    
    Args:
        username: Unique username
        email: User's email address
        
    Returns:
        int: The user_id of the newly created user
        
    Raises:
        sqlite3.IntegrityError: If username or email already exists
    """
    raise NotImplementedError("Students need to implement user insertion")


@module(dependencies=["create_movies_table"], difficulty="easy")
def insert_movie(movie_id: int, title: str, genres: str, release_year: int) -> None:
    """
    Insert a new movie into the database.
    
    Args:
        movie_id: Unique movie ID from dataset
        title: Movie title
        genres: Pipe-separated genres (e.g., "Action|Adventure|Sci-Fi")
        release_year: Year the movie was released
    """
    raise NotImplementedError("Students need to implement movie insertion")


@module(dependencies=["create_ratings_table"], difficulty="medium")
def insert_rating(user_id: int, movie_id: int, rating: float) -> None:
    """
    Insert or update a rating in the database.
    Also updates the movie's average_rating and rating_count.
    
    Args:
        user_id: ID of the user rating the movie
        movie_id: ID of the movie being rated
        rating: Rating value (0.5 to 5.0 in 0.5 increments)
        
    Hint: Use INSERT OR REPLACE for upsert behavior
    Hint: Update movie statistics (average_rating, rating_count) after insert
    """
    raise NotImplementedError("Students need to implement rating insertion with movie stats update")


@module(dependencies=["create_ratings_table"], difficulty="medium")
def get_user_ratings(user_id: int) -> List[Dict]:
    """
    Get all ratings made by a specific user.
    
    Args:
        user_id: ID of the user
        
    Returns:
        List of dicts with keys: movie_id, title, rating, timestamp, genres
    """
    raise NotImplementedError("Students need to implement fetching user ratings")


@module(dependencies=["create_ratings_table"], difficulty="medium")
def get_movie_ratings(movie_id: int) -> List[Dict]:
    """
    Get all ratings for a specific movie.
    
    Args:
        movie_id: ID of the movie
        
    Returns:
        List of dicts with keys: user_id, username, rating, timestamp
    """
    raise NotImplementedError("Students need to implement fetching movie ratings")


@module(dependencies=["create_movies_table"], difficulty="easy")
def search_movies(query: str, limit: int = 10) -> List[Dict]:
    """
    Search for movies by title (case-insensitive partial match).
    
    Args:
        query: Search string
        limit: Maximum number of results to return
        
    Returns:
        List of dicts with keys: movie_id, title, genres, release_year, average_rating
        
    Hint: Use LIKE with LOWER() for case-insensitive search
    """
    raise NotImplementedError("Students need to implement movie search")


@module(dependencies=["create_movies_table"], difficulty="easy")
def get_movie_details(movie_id: int) -> Optional[Dict]:
    """
    Get detailed information about a specific movie.
    
    Args:
        movie_id: ID of the movie
        
    Returns:
        Dict with keys: movie_id, title, genres, release_year, average_rating, rating_count
        None if movie not found
    """
    raise NotImplementedError("Students need to implement fetching movie details")
