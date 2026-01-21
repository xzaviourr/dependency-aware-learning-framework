"""
Tests for database layer modules.
"""
import pytest
import sqlite3
from projects.movie_recommendation_system.database import *


@pytest.mark.tests_module("create_database_connection")
def test_create_database_connection():
    """Test database connection creation."""
    conn, cursor = create_database_connection()
    assert conn is not None, "Connection should not be None"
    assert cursor is not None, "Cursor should not be None"
    # Test connection is active
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1
    cursor.close()
    conn.close()


@pytest.mark.tests_module("create_users_table")
def test_create_users_table():
    """Test users table creation."""
    create_users_table()
    # Verify table exists
    conn, cursor = create_database_connection()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    exists = cursor.fetchone() is not None
    assert exists, "Users table should exist"
    cursor.close()
    conn.close()


@pytest.mark.tests_module("create_movies_table")
def test_create_movies_table():
    """Test movies table creation."""
    create_movies_table()
    conn, cursor = create_database_connection()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='movies'
    """)
    exists = cursor.fetchone() is not None
    assert exists, "Movies table should exist"
    cursor.close()
    conn.close()


@pytest.mark.tests_module("create_ratings_table")
def test_create_ratings_table():
    """Test ratings table creation with foreign keys."""
    create_ratings_table()
    conn, cursor = create_database_connection()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='ratings'
    """)
    exists = cursor.fetchone() is not None
    assert exists, "Ratings table should exist"
    cursor.close()
    conn.close()


@pytest.mark.tests_module("insert_user")
def test_insert_user():
    """Test user insertion."""
    user_id = insert_user("test_user", "test@example.com")
    assert isinstance(user_id, int), "Should return user ID"
    assert user_id > 0, "User ID should be positive"


@pytest.mark.tests_module("insert_movie")
def test_insert_movie():
    """Test movie insertion."""
    insert_movie(1, "Test Movie (2020)", "Action|Adventure", 2020)
    # Verify insertion
    conn, cursor = create_database_connection()
    cursor.execute("SELECT title FROM movies WHERE movie_id = 1")
    result = cursor.fetchone()
    assert result is not None
    assert "Test Movie" in result[0]
    cursor.close()
    conn.close()


@pytest.mark.tests_module("insert_rating")
def test_insert_rating():
    """Test rating insertion and movie stats update."""
    # Assumes user and movie already exist from previous tests
    insert_rating(1, 1, 4.5)
    # Verify rating exists
    conn, cursor = create_database_connection()
    cursor.execute("SELECT rating FROM ratings WHERE user_id = 1 AND movie_id = 1")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 4.5
    cursor.close()
    conn.close()


@pytest.mark.tests_module("get_user_ratings")
def test_get_user_ratings():
    """Test fetching user ratings."""
    ratings = get_user_ratings(1)
    assert isinstance(ratings, list), "Should return a list"
    if len(ratings) > 0:
        assert "movie_id" in ratings[0]
        assert "rating" in ratings[0]
        assert "title" in ratings[0]


@pytest.mark.tests_module("get_movie_ratings")
def test_get_movie_ratings():
    """Test fetching movie ratings."""
    ratings = get_movie_ratings(1)
    assert isinstance(ratings, list), "Should return a list"
    if len(ratings) > 0:
        assert "user_id" in ratings[0]
        assert "rating" in ratings[0]


@pytest.mark.tests_module("search_movies")
def test_search_movies():
    """Test movie search functionality."""
    results = search_movies("Test", limit=5)
    assert isinstance(results, list), "Should return a list"
    assert len(results) <= 5, "Should respect limit parameter"
    if len(results) > 0:
        assert "movie_id" in results[0]
        assert "title" in results[0]


@pytest.mark.tests_module("get_movie_details")
def test_get_movie_details():
    """Test fetching movie details."""
    details = get_movie_details(1)
    if details is not None:
        assert isinstance(details, dict)
        assert "movie_id" in details
        assert "title" in details
        assert "average_rating" in details
