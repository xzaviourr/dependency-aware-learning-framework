# Quick Start Guide - Movie Recommendation System 🚀

## Installation (5 minutes)

### 1. Install PostgreSQL
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu
sudo apt install postgresql
sudo systemctl start postgresql
```

### 2. Install Python Dependencies
```bash
cd projects/movie_recommendation_system
pip install -r requirements.txt
```

### 3. Setup Database
```bash
createdb movie_recommendations
```

### 4. Download Kaggle Dataset
1. Go to: https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset
2. Download `movies.csv` and `ratings.csv`  
3. Place in `data/` directory

## Start Learning! 🎓

### Check What's Available
```bash
python -m framework.cli status
```

You'll see:
- 🟢 **Completed** - Tests passed
- 🟧 **Available** - Ready to implement (START HERE!)
- 🔴 **Locked** - Dependencies not met

### Implement First Module
Open `database.py` and implement `create_database_connection`:

```python
@module(dependencies=[], difficulty="easy")
def create_database_connection():
    """Create connection to PostgreSQL."""
    import psycopg2
    conn = psycopg2.connect(
        host="localhost",
        database="movie_recommendations",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    return conn, cursor
```

### Run Tests
```bash
pytest -v
```

If test passes: ✅ Module completed!  
Check `progress.md` for updated visualization.

### Get Next Steps
```bash
python -m framework.cli next
```

Shows suggested modules sorted by difficulty.

## Learning Path

**Phase 1: Database (Days 1-2)**
- Connection → Tables → CRUD operations

**Phase 2: Data Loading (Day 3)**  
- Load CSV files → Populate database

**Phase 3: Algorithms (Days 4-6)**
- Similarity calculations → Recommendation engines

**Phase 4: API (Days 7-8)**
- Flask endpoints → Complete REST API

## Hints & Tips

💡 **Stuck?** Check the docstring - it has implementation hints!  
💡 **Error?** Read test failures - they guide you  
💡 **Slow?** Load subset of data first (first 1000 movies/ratings)  
💡 **Progress?** Run `python -m framework.cli path` to see full learning path

## Need Help?

1. Read the function's docstring (has hints!)
2. Check `projects/movie_recommendation_system/README.md`
3. Run `python -m framework.cli status` to verify dependencies

Happy coding! 🎉
