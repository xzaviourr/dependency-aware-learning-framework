# Movie Recommendation System 🎬

A comprehensive movie recommendation system project designed for learning. Students will implement a complete recommendation engine from database design to RESTful APIs, using real movie data.

## 📚 Learning Objectives

By completing this project, you will learn:
- PostgreSQL database design and operations
- Data loading from CSV files
- Collaborative filtering algorithms (user-based and item-based)
- Content-based filtering
- Hybrid recommendation approaches
- RESTful API development with Flask
- Real-world data processing and analysis

## 🎯 Project Structure

The project is divided into **39 modules** across 4 layers:

### 1. Database Layer (`database.py`) - 11 modules
- Database connection setup
- Table creation (users, movies, ratings)
- CRUD operations
- Search and retrieval functions

### 2. Data Loading (`data_loader.py`) - 5 modules
- CSV file parsing
- Bulk data insertion
- User generation
- Statistics calculation

### 3. Recommendation Algorithms (`algorithms.py`) - 8 modules
- User similarity calculation (cosine similarity)
- Movie similarity calculation
- User-based collaborative filtering
- Item-based collaborative filtering
- Content-based recommendations
- Hybrid recommendations
- Personalized recommendations

### 4. API Layer (`api.py`) - 10 modules
- Flask application setup
- Rating submission endpoint
- Recommendation endpoints (multiple algorithms)
- Movie search and details
- User profile management
- Statistics endpoints

## 🚀 Getting Started

### Prerequisites

1. **Python 3.9+** (SQLite3 is included in Python standard library)

2. **Python packages**
   ```bash
   pip install flask flask-cors numpy pandas
   ```

3. **Kaggle Dataset** - Download the MovieLens dataset:
   - Go to: https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset
   - Download `movies.csv` and `ratings.csv`
   - Create a `data/` directory in this project
   - Place the CSV files there

### Database Setup

SQLite database file (`movie_recommendations.db`) will be created automatically when you run the first module. No manual setup required!

## 📖 Learning Path

Run this command to see suggested modules:
```bash
python -m framework.cli status
```

**Recommended progression:**

1. **Start with Database** (Easy)
   - `create_database_connection` ← Start here!
   - `create_users_table`
   - `create_movies_table`
   - `create_ratings_table`

2. **Basic Operations** (Easy-Medium)
   - `insert_user`, `insert_movie`, `insert_rating`
   - `get_user_ratings`, `get_movie_ratings`
   - `search_movies`, `get_movie_details`

3. **Load Data** (Medium-Hard)
   - `load_movies_from_csv`
   - `generate_sample_users`
   - `load_ratings_from_csv` (Warning: may take time!)
   - `update_movie_statistics`

4. **Implement Algorithms** (Hard)
   - `calculate_user_similarity`
   - `calculate_movie_similarity`
   - `get_user_based_recommendations`
   - `get_item_based_recommendations`
   - `get_content_based_recommendations`
   - `get_hybrid_recommendations`

5. **Build API** (Medium)
   - `create_flask_app`
   - All endpoint functions
   - `run_flask_app`

## 🧪 Testing

Run tests for completed modules:
```bash
pytest
```

Check progress:
```bash
python -m framework.cli status
python -m framework.cli next  # See what to work on
```

View progress visualization:
```bash
# Opens progress.md with dependency graph
cat progress.md
```

## 📊 Dataset Information

**MovieLens Dataset:**
- ~27,000 movies
- ~138,000 users
- ~20 million ratings
- Ratings: 0.5 to 5.0 stars

**Note:** For faster development, consider loading only a subset:
- First 5,000 movies
- First 10,000 users
- First 100,000 ratings

## 🔧 API Endpoints (Final Result)

Once completed, your API will have:

```
POST   /api/users/register          - Register new user
POST   /api/ratings                 - Submit a rating
GET    /api/recommendations/:id     - Get personalized recommendations
GET    /api/movies/search           - Search movies
GET    /api/movies/:id              - Get movie details
GET    /api/movies/:id/similar      - Get similar movies
GET    /api/users/:id/profile       - Get user profile
GET    /api/stats                   - Get dataset statistics
```

## 💡 Implementation Tips

### Database Layer
- Enable foreign keys: `PRAGMA foreign_keys = ON;`
- Create indexes on foreign keys for better performance
- Use transactions for data consistency
- Use `executemany()` for batch operations

### Data Loading
- Use batch inserts with `executemany()` (1000 rows at a time)
- Add progress logging for large datasets
- Consider using transactions for faster bulk loading

### Algorithms
- Cache similarity calculations
- Use numpy for matrix operations
- Set minimum thresholds to filter noise

### API Layer
- Validate all inputs
- Use proper HTTP status codes
- Add rate limiting for production
- Enable CORS for frontend access

## 🎓 Learning Resources

- **SQLite**: https://www.sqlite.org/docs.html
- **Python sqlite3**: https://docs.python.org/3/library/sqlite3.html
- **Flask**: https://flask.palletsprojects.com/
- **Collaborative Filtering**: https://en.wikipedia.org/wiki/Collaborative_filtering
- **Cosine Similarity**: https://en.wikipedia.org/wiki/Cosine_similarity

## 📈 Progress Tracking

Your progress is automatically tracked:
- ✅ Completed modules (tests passed)
- 🟧 Available modules (dependencies met)
- 🔴 Locked modules (complete prerequisites first)

Check `progress.md` file for visual dependency graph!

## 🐛 Common Issues

**Issue:** Database connection fails
- Solution: Check file permissions for `movie_recommendations.db`
- Solution: Ensure you're running from the project directory

**Issue:** CSV loading is slow
- Solution: Load subset of data for testing
- Solution: Use batch inserts and `execute_batch()`

**Issue:** Tests fail with "dependencies not met"
- Solution: Complete prerequisite modules first
- Solution: Check `python -m framework.cli status`

## 📝 License

MIT License - Educational Use
