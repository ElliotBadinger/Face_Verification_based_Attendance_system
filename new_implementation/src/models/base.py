from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

Base = declarative_base()

class AuditMixin:
    """Mixin for audit trail on all models"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    updated_by = Column(String(100))

class POPIAMixin:
    """Mixin for POPIA compliance features"""
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime)
    data_retention_date = Column(DateTime)
    purpose_of_collection = Column(String(500))
    data_access_log = Column(String(1000))  # JSON string of access logs
    
    def log_access(self, user_id: str, purpose: str):
        """Log data access as required by POPIA"""
        access_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "purpose": purpose
        }
        # In production, implement proper access logging
        pass

    def verify_consent(self) -> bool:
        """Verify if consent is valid and not expired"""
        if not self.consent_given:
            return False
        if self.data_retention_date and datetime.utcnow() > self.data_retention_date:
            return False
        return True
