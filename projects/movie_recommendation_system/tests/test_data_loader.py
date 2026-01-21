"""
Tests for data loading modules.
"""
import pytest
from pathlib import Path
from projects.movie_recommendation_system.data_loader import *


@pytest.mark.tests_module("load_movies_from_csv")
def test_load_movies_from_csv():
    """Test loading movies from CSV file."""
    # Students should have downloaded the Kaggle dataset
    csv_path = "data/movies.csv"
    if not Path(csv_path).exists():
        pytest.skip("Kaggle dataset not found. Download from Kaggle first.")
    
    count = load_movies_from_csv(csv_path)
    assert isinstance(count, int), "Should return number of movies loaded"
    assert count > 0, "Should load at least some movies"


@pytest.mark.tests_module("generate_sample_users")
def test_generate_sample_users():
    """Test sample user generation."""
    count = generate_sample_users(50)
    assert isinstance(count, int), "Should return number of users created"
    assert count == 50, "Should create exactly 50 users"


@pytest.mark.tests_module("load_ratings_from_csv")
def test_load_ratings_from_csv():
    """Test loading ratings from CSV file."""
    csv_path = "data/ratings.csv"
    if not Path(csv_path).exists():
        pytest.skip("Kaggle dataset not found. Download from Kaggle first.")
    
    # Load a subset for testing (first 1000 rows)
    count = load_ratings_from_csv(csv_path)
    assert isinstance(count, int), "Should return number of ratings loaded"
    assert count > 0, "Should load at least some ratings"


@pytest.mark.tests_module("update_movie_statistics")
def test_update_movie_statistics():
    """Test updating movie statistics."""
    update_movie_statistics()
    # Verify some movie has updated stats
    from projects.movie_recommendation_system.database import get_movie_details
    details = get_movie_details(1)
    if details:
        assert details["rating_count"] >= 0, "Rating count should be non-negative"
        assert 0 <= details["average_rating"] <= 5, "Average rating should be between 0 and 5"


@pytest.mark.tests_module("get_dataset_statistics")
def test_get_dataset_statistics():
    """Test dataset statistics calculation."""
    stats = get_dataset_statistics()
    assert isinstance(stats, dict), "Should return a dictionary"
    assert "total_movies" in stats
    assert "total_users" in stats
    assert "total_ratings" in stats
    assert stats["total_movies"] > 0, "Should have some movies"
    assert stats["total_users"] > 0, "Should have some users"
