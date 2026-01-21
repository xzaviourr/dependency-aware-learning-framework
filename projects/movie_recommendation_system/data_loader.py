"""
Data loading module for importing Kaggle MovieLens dataset.
Students will implement CSV parsing and bulk database population.
"""
import csv
from pathlib import Path
from typing import List, Dict
from framework.decorators import module


@module(dependencies=["create_movies_table", "create_users_table", "create_ratings_table"], difficulty="medium")
def load_movies_from_csv(csv_path: str) -> int:
    """
    Load movies from Kaggle CSV file into the database.
    
    Expected CSV format (movies.csv):
    movieId,title,genres
    1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
    
    Args:
        csv_path: Path to the movies.csv file
        
    Returns:
        int: Number of movies loaded
        
    Hint: Extract year from title using regex: r'\((\d{4})\)'
    Hint: Use executemany() for batch inserts
    """
    raise NotImplementedError("Students need to implement loading movies from CSV")


@module(dependencies=["create_users_table"], difficulty="medium")
def generate_sample_users(count: int = 100) -> int:
    """
    Generate sample users since Kaggle dataset only has user IDs.
    
    Args:
        count: Number of users to generate
        
    Returns:
        int: Number of users created
        
    Hint: Generate usernames like "user_1", "user_2", etc.
    Hint: Generate emails like "user_1@example.com"
    """
    raise NotImplementedError("Students need to implement user generation")


@module(dependencies=["load_movies_from_csv", "generate_sample_users"], difficulty="hard")
def load_ratings_from_csv(csv_path: str, user_mapping: Dict[int, int] = None) -> int:
    """
    Load ratings from Kaggle CSV file into the database.
    
    Expected CSV format (ratings.csv):
    userId,movieId,rating,timestamp
    1,1,4.0,964982703
    
    Args:
        csv_path: Path to the ratings.csv file
        user_mapping: Optional mapping of Kaggle user IDs to database user IDs
                     If None, create mapping on the fly
        
    Returns:
        int: Number of ratings loaded
        
    Note: This may take time for large datasets. Consider:
    - Batch inserts (e.g., 1000 rows at a time)
    - Progress logging every 10,000 rows
    - Filtering to only load subset of data for testing
    """
    raise NotImplementedError("Students need to implement loading ratings from CSV")


@module(dependencies=["load_ratings_from_csv"], difficulty="medium")
def update_movie_statistics() -> None:
    """
    Update average_rating and rating_count for all movies based on ratings table.
    
    This should be run after bulk loading ratings to populate the denormalized stats.
    
    Hint: Use SQL aggregation:
    UPDATE movies SET 
        average_rating = (SELECT AVG(rating) FROM ratings WHERE movie_id = movies.movie_id),
        rating_count = (SELECT COUNT(*) FROM ratings WHERE movie_id = movies.movie_id)
    """
    raise NotImplementedError("Students need to implement updating movie statistics")


@module(dependencies=["load_movies_from_csv", "load_ratings_from_csv"], difficulty="easy")
def get_dataset_statistics() -> Dict:
    """
    Get statistics about the loaded dataset.
    
    Returns:
        Dict with keys:
        - total_movies: Number of movies in database
        - total_users: Number of users
        - total_ratings: Number of ratings
        - avg_ratings_per_user: Average ratings per user
        - avg_ratings_per_movie: Average ratings per movie
        - rating_density: Percentage of possible ratings that exist
    """
    raise NotImplementedError("Students need to implement dataset statistics")
