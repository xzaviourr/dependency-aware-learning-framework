"""
Tests for recommendation algorithm modules.
"""
import pytest
from projects.movie_recommendation_system.algorithms import *


@pytest.mark.tests_module("calculate_user_similarity")
def test_calculate_user_similarity():
    """Test user similarity calculation."""
    # Assumes users 1 and 2 exist with ratings
    similarity = calculate_user_similarity(1, 2)
    assert isinstance(similarity, float), "Should return a float"
    assert 0 <= similarity <= 1, "Similarity should be between 0 and 1"


@pytest.mark.tests_module("calculate_movie_similarity")
def test_calculate_movie_similarity():
    """Test movie similarity calculation."""
    # Assumes movies 1 and 2 exist with ratings
    similarity = calculate_movie_similarity(1, 2)
    assert isinstance(similarity, float), "Should return a float"
    assert 0 <= similarity <= 1, "Similarity should be between 0 and 1"


@pytest.mark.tests_module("get_user_based_recommendations")
def test_get_user_based_recommendations():
    """Test user-based collaborative filtering."""
    recommendations = get_user_based_recommendations(1, top_n=5)
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) <= 5, "Should respect top_n parameter"
    if len(recommendations) > 0:
        assert "movie_id" in recommendations[0]
        assert "title" in recommendations[0]
        assert "predicted_rating" in recommendations[0]
        # Verify sorted by predicted_rating
        if len(recommendations) > 1:
            assert recommendations[0]["predicted_rating"] >= recommendations[1]["predicted_rating"]


@pytest.mark.tests_module("get_item_based_recommendations")
def test_get_item_based_recommendations():
    """Test item-based collaborative filtering."""
    recommendations = get_item_based_recommendations(1, top_n=5)
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) <= 5, "Should respect top_n parameter"
    if len(recommendations) > 0:
        assert "movie_id" in recommendations[0]
        assert "similarity_score" in recommendations[0]


@pytest.mark.tests_module("get_content_based_recommendations")
def test_get_content_based_recommendations():
    """Test content-based filtering."""
    recommendations = get_content_based_recommendations(1, top_n=5)
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) <= 5, "Should respect top_n parameter"
    if len(recommendations) > 0:
        assert "movie_id" in recommendations[0]
        assert "genre_overlap" in recommendations[0]


@pytest.mark.tests_module("get_hybrid_recommendations")
def test_get_hybrid_recommendations():
    """Test hybrid recommendation algorithm."""
    recommendations = get_hybrid_recommendations(1, top_n=5, user_weight=0.6)
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) <= 5, "Should respect top_n parameter"
    if len(recommendations) > 0:
        assert "movie_id" in recommendations[0]
        assert "hybrid_score" in recommendations[0]
        # Verify sorted by hybrid_score
        if len(recommendations) > 1:
            assert recommendations[0]["hybrid_score"] >= recommendations[1]["hybrid_score"]


@pytest.mark.tests_module("calculate_user_preference_vector")
def test_calculate_user_preference_vector():
    """Test user preference vector calculation."""
    preferences = calculate_user_preference_vector(1)
    assert isinstance(preferences, dict), "Should return a dictionary"
    # All preference values should be between 0 and 1
    for genre, score in preferences.items():
        assert isinstance(genre, str)
        assert 0 <= score <= 1, f"Preference score for {genre} should be between 0 and 1"


@pytest.mark.tests_module("get_personalized_recommendations")
def test_get_personalized_recommendations():
    """Test personalized recommendations."""
    recommendations = get_personalized_recommendations(1, top_n=5)
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) <= 5, "Should respect top_n parameter"
    if len(recommendations) > 0:
        assert "movie_id" in recommendations[0]
        assert "personalization_score" in recommendations[0]
        assert "average_rating" in recommendations[0]
