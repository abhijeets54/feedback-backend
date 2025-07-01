#!/usr/bin/env python3
"""
Railway startup script with better error handling
"""
import os
import sys
import time
from sqlalchemy import create_engine, text

def wait_for_db():
    """Wait for database to be ready"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    print("🔄 Waiting for database connection...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Database connection attempt {retry_count}/{max_retries} failed: {e}")
            time.sleep(2)
    
    print("❌ Database connection failed after all retries")
    return False

def main():
    """Main startup function"""
    print("🚀 Starting Employee Feedback Management System")
    print("=" * 50)
    
    # Check environment
    port = os.getenv("PORT", "8000")
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"Environment: {environment}")
    print(f"Port: {port}")
    
    # Wait for database
    if not wait_for_db():
        print("❌ Startup failed - database not available")
        sys.exit(1)
    
    # Start the application
    print("🚀 Starting FastAPI application...")
    os.system(f"python -m uvicorn main:app --host 0.0.0.0 --port {port}")

if __name__ == "__main__":
    main()
