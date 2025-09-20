# Bonus Feature 2: Database Integration with SQLAlchemy

from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/financial_analyzer_db')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(String, default=True)
    subscription_tier = Column(String, default="free")  # free, premium, enterprise

class AnalysisResult(Base):
    """Model for storing financial analysis results"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Foreign key to users table
    task_id = Column(String, unique=True, index=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    original_query = Column(Text, nullable=False)
    analysis_text = Column(Text, nullable=False)
    processing_time = Column(Float, nullable=True)  # Time in seconds
    status = Column(String, default="completed")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class DocumentUpload(Base):
    """Model for tracking document uploads"""
    __tablename__ = "document_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    task_id = Column(String, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(String, default=False)
    
class APIUsage(Base):
    """Model for tracking API usage and rate limiting"""
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    endpoint = Column(String, nullable=False)
    request_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    processing_time = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=False)
    file_size = Column(Integer, nullable=True)
    
# Database utility functions
def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_user_by_email(db: Session, email: str):
    """Get user by email address"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, username: str):
    """Create a new user"""
    db_user = User(email=email, username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def save_analysis_result(db: Session, task_id: str, user_id: int, file_name: str, 
                        query: str, analysis: str, processing_time: float, status: str = "completed"):
    """Save analysis result to database"""
    db_result = AnalysisResult(
        task_id=task_id,
        user_id=user_id,
        file_name=file_name,
        original_query=query,
        analysis_text=analysis,
        processing_time=processing_time,
        status=status
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_analysis_result(db: Session, task_id: str):
    """Retrieve analysis result by task ID"""
    return db.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()

def get_user_analysis_history(db: Session, user_id: int, limit: int = 10):
    """Get user's analysis history"""
    return db.query(AnalysisResult).filter(
        AnalysisResult.user_id == user_id
    ).order_by(AnalysisResult.created_at.desc()).limit(limit).all()

def log_document_upload(db: Session, user_id: int, task_id: str, filename: str, 
                       file_path: str, file_size: int, content_type: str):
    """Log document upload to database"""
    db_upload = DocumentUpload(
        user_id=user_id,
        task_id=task_id,
        original_filename=filename,
        file_path=file_path,
        file_size=file_size,
        content_type=content_type
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    return db_upload

def log_api_usage(db: Session, user_id: int, endpoint: str, processing_time: float, 
                 status_code: int, file_size: int = None):
    """Log API usage for analytics and rate limiting"""
    db_usage = APIUsage(
        user_id=user_id,
        endpoint=endpoint,
        processing_time=processing_time,
        status_code=status_code,
        file_size=file_size
    )
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage

def get_user_usage_stats(db: Session, user_id: int, days: int = 30):
    """Get user usage statistics for the last N days"""
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    usage_stats = db.query(APIUsage).filter(
        APIUsage.user_id == user_id,
        APIUsage.request_timestamp >= cutoff_date
    ).all()
    
    total_requests = len(usage_stats)
    avg_processing_time = sum(u.processing_time for u in usage_stats if u.processing_time) / total_requests if total_requests > 0 else 0
    total_file_size = sum(u.file_size for u in usage_stats if u.file_size) or 0
    
    return {
        'total_requests': total_requests,
        'avg_processing_time': avg_processing_time,
        'total_file_size_mb': total_file_size / (1024 * 1024),
        'period_days': days
    }

# Pydantic models for API responses
from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    username: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    subscription_tier: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class AnalysisResultResponse(BaseModel):
    id: int
    task_id: str
    file_name: str
    original_query: str
    status: str
    processing_time: Optional[float]
    created_at: datetime
    
    class Config:
        orm_mode = True

class UsageStatsResponse(BaseModel):
    total_requests: int
    avg_processing_time: float
    total_file_size_mb: float
    period_days: int