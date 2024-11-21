from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, AuditMixin, POPIAMixin

class Student(Base, AuditMixin, POPIAMixin):
    """Student model with POPIA compliance and cultural considerations"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(String(100), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    grade = Column(String(20))
    parent_id = Column(Integer, ForeignKey("users.id"))
    
    # POPIA and Privacy
    face_data_consent = Column(Boolean, default=False)
    face_data_consent_date = Column(DateTime)
    face_data_expiry = Column(DateTime)
    data_processing_consent = Column(Boolean, default=False)
    
    # Cultural and Religious Considerations
    cultural_considerations = Column(JSON)  # Store as JSON for flexibility
    religious_accommodations = Column(JSON)  # Store as JSON for flexibility
    
    # Notification Preferences
    notification_preferences = Column(JSON, default={
        "attendance_alerts": True,
        "late_arrival_alerts": True,
        "unauthorized_exit_alerts": True,
        "method": "email"  # or sms, app_notification
    })
    
    # Relationships
    parent = relationship("User", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student")
    face_data = relationship("FaceData", back_populates="student")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purpose_of_collection = "Student identification and attendance tracking"
        
    def update_cultural_consideration(self, consideration_type: str, details: dict):
        """Update cultural considerations"""
        if self.cultural_considerations is None:
            self.cultural_considerations = {}
        self.cultural_considerations[consideration_type] = {
            "details": details,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def has_valid_face_consent(self) -> bool:
        """Check if face recognition consent is valid"""
        if not self.face_data_consent:
            return False
        if self.face_data_expiry and datetime.utcnow() > self.face_data_expiry:
            return False
        return True
    
    def get_attendance_notification_recipients(self) -> list:
        """Get list of notification recipients based on preferences"""
        recipients = []
        if self.parent and self.notification_preferences.get("attendance_alerts"):
            recipients.append({
                "id": self.parent.id,
                "method": self.notification_preferences.get("method", "email"),
                "contact": self.parent.email if self.notification_preferences.get("method") == "email" 
                          else self.parent.phone_number
            })
        return recipients

    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
