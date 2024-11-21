from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .base import Base, AuditMixin, POPIAMixin

class FaceData(Base, AuditMixin, POPIAMixin):
    """Face data model with encryption and privacy features"""
    __tablename__ = "face_data"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    # Encrypted face encoding data
    encoding_data = Column(LargeBinary)
    encryption_key_id = Column(String(100))  # Reference to encryption key in secure storage
    encryption_version = Column(String(50))  # For encryption version tracking
    
    # Privacy and Security
    valid_until = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=365))
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime)
    usage_count = Column(Integer, default=0)
    
    # Data quality and verification
    quality_score = Column(Integer)  # Score of face encoding quality
    verification_status = Column(String(50))  # Status of last verification
    last_verification = Column(DateTime)
    
    # Relationships
    student = relationship("Student", back_populates="face_data")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purpose_of_collection = "Facial recognition for secure attendance tracking"
        
    def is_valid(self) -> bool:
        """Check if face data is valid and not expired"""
        if not self.is_active:
            return False
        if datetime.utcnow() > self.valid_until:
            return False
        return True
    
    def record_usage(self):
        """Record usage of face data"""
        self.usage_count += 1
        self.last_used = datetime.utcnow()
        
    def needs_reverification(self) -> bool:
        """Check if face data needs reverification"""
        if not self.last_verification:
            return True
        # Require reverification if:
        # 1. Last verification was more than 90 days ago
        # 2. Usage count exceeded 1000
        # 3. Quality score is below threshold
        if (datetime.utcnow() - self.last_verification).days > 90:
            return True
        if self.usage_count > 1000:
            return True
        if self.quality_score and self.quality_score < 80:
            return True
        return False
    
    def update_verification_status(self, status: str, quality_score: int = None):
        """Update verification status and quality score"""
        self.verification_status = status
        if quality_score is not None:
            self.quality_score = quality_score
        self.last_verification = datetime.utcnow()
    
    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
