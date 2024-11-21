from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base, AuditMixin

class UserRole(enum.Enum):
    """User role definitions"""
    ADMIN = "admin"
    TEACHER = "teacher"
    PARENT = "parent"
    SECURITY = "security"  # For security personnel managing gate cameras

class User(Base, AuditMixin):
    """User model with enhanced security features"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    phone_number = Column(String(20))
    
    # Security features
    last_login = Column(String(100))
    failed_login_attempts = Column(Integer, default=0)
    password_last_changed = Column(DateTime, default=datetime.utcnow)
    requires_password_change = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(100))
    
    # Access control
    allowed_gates = Column(String(500))  # JSON string of gate IDs
    access_hours = Column(String(500))  # JSON string of allowed access hours
    
    # Relationships
    students = relationship("Student", back_populates="parent")
    audit_logs = relationship("AuditLog", back_populates="user")

    def increment_failed_login(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.is_active = False
            # In production, implement notification system
    
    def reset_failed_login(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        self.last_login = datetime.utcnow().isoformat()
    
    def check_password_expiry(self) -> bool:
        """Check if password needs to be changed"""
        password_age = datetime.utcnow() - self.password_last_changed
        return password_age.days > 90  # Force password change every 90 days
    
    def has_gate_access(self, gate_id: str) -> bool:
        """Check if user has access to specific gate"""
        if self.role == UserRole.ADMIN:
            return True
        # In production, implement proper gate access checking
        return True
