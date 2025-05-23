from database import Base, engine
from app.models import PredictionLog

def reset_db():
    # # Drop all tables
    # Base.metadata.drop_all(bind=engine)
    # print("All tables dropped.")
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    reset_db()