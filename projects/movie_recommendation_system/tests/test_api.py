"""
Tests for API layer modules.
"""
import pytest
import json
from flask import Flask
from projects.movie_recommendation_system.api import *


@pytest.fixture
def test_app():
    """Create a test Flask app."""
    app = create_flask_app()
    app.config['TESTING'] = True
    return app


@pytest.mark.tests_module("create_flask_app")
def test_create_flask_app():
    """Test Flask app creation."""
    app = create_flask_app()
    assert isinstance(app, Flask), "Should return a Flask instance"
    assert app is not None


@pytest.mark.tests_module("add_rating_endpoint")
def test_add_rating_endpoint(test_app):
    """Test rating endpoint."""
    add_rating_endpoint(test_app)
    client = test_app.test_client()
    
    # Test valid rating
    response = client.post('/api/ratings', 
                          data=json.dumps({"user_id": 1, "movie_id": 1, "rating": 4.5}),
                          content_type='application/json')
    assert response.status_code in [200, 201], "Should accept valid rating"


@pytest.mark.tests_module("get_recommendations_endpoint")
def test_get_recommendations_endpoint(test_app):
    """Test recommendations endpoint."""
    get_recommendations_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/recommendations/1?count=5')
    assert response.status_code == 200, "Should return recommendations"
    data = json.loads(response.data)
    assert "recommendations" in data


@pytest.mark.tests_module("get_movie_details_endpoint")
def test_get_movie_details_endpoint(test_app):
    """Test movie details endpoint."""
    get_movie_details_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/movies/1')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert "movie_id" in data
        assert "title" in data


@pytest.mark.tests_module("search_movies_endpoint")
def test_search_movies_endpoint(test_app):
    """Test movie search endpoint."""
    search_movies_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/movies/search?q=test&limit=5')
    assert response.status_code == 200, "Should return search results"
    data = json.loads(response.data)
    assert "results" in data


@pytest.mark.tests_module("get_user_profile_endpoint")
def test_get_user_profile_endpoint(test_app):
    """Test user profile endpoint."""
    get_user_profile_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/users/1/profile')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert "user_id" in data
        assert "total_ratings" in data


@pytest.mark.tests_module("register_user_endpoint")
def test_register_user_endpoint(test_app):
    """Test user registration endpoint."""
    register_user_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.post('/api/users/register',
                          data=json.dumps({"username": "testuser123", "email": "test123@example.com"}),
                          content_type='application/json')
    assert response.status_code in [200, 201, 409], "Should handle registration"


@pytest.mark.tests_module("get_similar_movies_endpoint")
def test_get_similar_movies_endpoint(test_app):
    """Test similar movies endpoint."""
    get_similar_movies_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/movies/1/similar?count=5')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert "similar_movies" in data


@pytest.mark.tests_module("get_stats_endpoint")
def test_get_stats_endpoint(test_app):
    """Test statistics endpoint."""
    get_stats_endpoint(test_app)
    client = test_app.test_client()
    
    response = client.get('/api/stats')
    assert response.status_code == 200, "Should return statistics"
    data = json.loads(response.data)
    assert "total_movies" in data
    assert "total_users" in data


@pytest.mark.tests_module("run_flask_app")
def test_run_flask_app():
    """Test Flask app runner."""
    # This is a smoke test - actual running would block
    app = create_flask_app()
    # Just verify the function exists and doesn't crash with parameters
    try:
        # Don't actually run the app in tests
        assert callable(run_flask_app), "run_flask_app should be callable"
    except NotImplementedError:
        pytest.skip("run_flask_app not yet implemented")
