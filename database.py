import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

def test_connection_details():
    """Print and verify database connection details."""
    url = urlparse(DATABASE_URL)
    print("\nConnection Details:")
    print(f"Host: {url.hostname}")
    print(f"Port: {url.port}")
    print(f"Database: {url.path[1:]}")
    return True

# Configure SQLAlchemy for Supabase connection
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 30,
        "application_name": "diabetes_api"
    },
    pool_size=20,
    max_overflow=0
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """Database dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connectivity and provide troubleshooting tips."""
    try:
        test_connection_details()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print("\nDatabase connection successful! ✓")
            return True
    except Exception as e:
        print(f"\nConnection error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if port 6543 is open (not 5432)")
        print("2. Verify your connection string in Supabase dashboard")
        print("3. Try connecting with psql to test credentials")
        print("4. Check if your IP is allowlisted in Supabase")
        return False

if __name__ == "__main__":
    test_connection()