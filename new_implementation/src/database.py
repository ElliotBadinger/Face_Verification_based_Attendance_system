from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
import logging
from typing import Generator

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./attendance_system.db"  # Default to SQLite for development
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Adjust based on expected concurrent connections
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections every 30 minutes
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

@contextmanager
def get_db() -> Generator:
    """Get database session with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """Initialize database with tables"""
    try:
        # Import all models to ensure they're registered
        from models.user import User
        from models.student import Student
        from models.face_data import FaceData
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

def check_db_connection() -> bool:
    """Check database connection"""
    try:
        with get_db() as db:
            db.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False

class DatabaseManager:
    """Manager class for database operations"""
    
    @staticmethod
    async def get_connection():
        """Get database connection"""
        return get_db()
    
    @staticmethod
    async def backup_database(backup_path: str):
        """Create database backup"""
        try:
            if DATABASE_URL.startswith('sqlite'):
                import shutil
                db_path = DATABASE_URL.replace('sqlite:///', '')
                shutil.copy2(db_path, backup_path)
                logger.info(f"Database backed up to {backup_path}")
            else:
                # Implement backup for other database types
                raise NotImplementedError("Backup not implemented for this database type")
        except Exception as e:
            logger.error(f"Database backup failed: {str(e)}")
            raise
    
    @staticmethod
    async def restore_database(backup_path: str):
        """Restore database from backup"""
        try:
            if DATABASE_URL.startswith('sqlite'):
                import shutil
                db_path = DATABASE_URL.replace('sqlite:///', '')
                shutil.copy2(backup_path, db_path)
                logger.info(f"Database restored from {backup_path}")
            else:
                # Implement restore for other database types
                raise NotImplementedError("Restore not implemented for this database type")
        except Exception as e:
            logger.error(f"Database restore failed: {str(e)}")
            raise

# Database migration configuration
MIGRATION_DIR = os.path.join(os.path.dirname(__file__), 'migrations')
if not os.path.exists(MIGRATION_DIR):
    os.makedirs(MIGRATION_DIR)

# Alembic configuration (if using migrations)
ALEMBIC_CONFIG = {
    'script_location': MIGRATION_DIR,
    'sqlalchemy.url': DATABASE_URL,
    'target_metadata': Base.metadata
}
