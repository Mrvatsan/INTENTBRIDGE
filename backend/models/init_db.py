"""
Database initialization script for IntentBridge.

Creates all database tables defined in the ORM models. In production,
consider using Alembic for migrations instead of this script.
"""
from sqlalchemy import create_engine
from backend.core.config import settings
from backend.models.database import Base
import logging

def init_db():
    if not settings.DATABASE_URL:
        logging.error("DATABASE_URL not set")
        return
    
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    # In a real setup, we'd use Alembic. 
    # This is for the initialization demonstration.
    pass
