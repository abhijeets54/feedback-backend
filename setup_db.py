import os
import getpass
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.models import Base, User, Feedback, UserRole, SentimentType
from app.auth import get_password_hash

def setup_database():
    # Get password from user
    password = getpass.getpass("Enter PostgreSQL password for user 'postgres': ")
    
    # Create connection string
    database_url = f"postgresql://postgres:{password}@localhost:5432/feedback_db"
    
    # Update .env file
    with open('.env', 'w') as f:
        f.write(f"DATABASE_URL={database_url}\n")
        f.write("SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7\n")
        f.write("ALGORITHM=HS256\n")
        f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
    
    # Test connection and create tables
    try:
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Seed data
        seed_database(engine)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def seed_database(engine):
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if any users already exist
        if db.query(User).first():
            print("Database already has users - skipping seeding!")
            print("For real-world usage, create users through the registration endpoint or admin interface.")
            return

        print("Database is empty and ready for real users!")
        print("No demo/mock data will be created.")
        print("\nTo add real users, you can:")
        print("1. Use the registration endpoint: POST /api/auth/register")
        print("2. Create users directly in the database")
        print("3. Import users from your existing system")

        # No demo data creation - database remains clean for real usage
        print("✅ Database setup completed!")
        print("Database is ready for real users and feedback data.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
