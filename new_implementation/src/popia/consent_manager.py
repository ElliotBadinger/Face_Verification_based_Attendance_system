from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class ConsentType(Enum):
    """Types of consent required"""
    FACE_RECOGNITION = "face_recognition"
    DATA_RETENTION = "data_retention"
    NOTIFICATIONS = "notifications"
    DATA_SHARING = "data_sharing"
    CULTURAL_ACCOMMODATION = "cultural_accommodation"

class ConsentStatus(Enum):
    """Status of consent"""
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"
    PENDING = "pending"

class ConsentManager:
    """Manages POPIA compliance for consent"""
    
    def __init__(self, db_session):
        self.db_session = db_session
        
    async def record_consent(
        self,
        student_id: int,
        consent_type: ConsentType,
        given_by: str,
        valid_until: Optional[datetime] = None,
        additional_details: Optional[Dict] = None
    ) -> Dict:
        """Record a new consent entry"""
        if valid_until is None:
            valid_until = datetime.utcnow() + timedelta(days=365)
            
        consent_record = {
            "student_id": student_id,
            "consent_type": consent_type.value,
            "given_by": given_by,
            "given_at": datetime.utcnow().isoformat(),
            "valid_until": valid_until.isoformat(),
            "status": ConsentStatus.ACTIVE.value,
            "purpose": self._get_purpose(consent_type),
            "additional_details": additional_details or {}
        }
        
        # In production: Save to database and audit log
        logger.info(f"Recorded consent: {consent_record}")
        return consent_record

    def verify_consent(
        self,
        student_id: int,
        consent_type: ConsentType
    ) -> bool:
        """Verify if valid consent exists"""
        # In production: Check database for valid consent
        return True

    async def withdraw_consent(
        self,
        student_id: int,
        consent_type: ConsentType,
        withdrawn_by: str,
        reason: Optional[str] = None
    ):
        """Handle consent withdrawal"""
        withdrawal_record = {
            "student_id": student_id,
            "consent_type": consent_type.value,
            "withdrawn_by": withdrawn_by,
            "withdrawn_at": datetime.utcnow().isoformat(),
            "reason": reason
        }
        
        # In production:
        # 1. Update consent status in database
        # 2. Trigger data deletion if required
        # 3. Update audit log
        # 4. Notify relevant parties
        
        logger.info(f"Consent withdrawn: {withdrawal_record}")

    def _get_purpose(self, consent_type: ConsentType) -> str:
        """Get purpose description for consent type"""
        purposes = {
            ConsentType.FACE_RECOGNITION: "Facial recognition for secure attendance tracking",
            ConsentType.DATA_RETENTION: "Storage of attendance and identification data",
            ConsentType.NOTIFICATIONS: "Sending attendance notifications to parents/guardians",
            ConsentType.DATA_SHARING: "Sharing attendance data with authorized school staff",
            ConsentType.CULTURAL_ACCOMMODATION: "Recording cultural/religious accommodation requirements"
        }
        return purposes.get(consent_type, "General purpose")

    async def handle_data_access_request(
        self,
        student_id: int,
        requested_by: str,
        data_types: List[str]
    ) -> Dict:
        """Handle POPIA data access request"""
        request_record = {
            "student_id": student_id,
            "requested_by": requested_by,
            "requested_at": datetime.utcnow().isoformat(),
            "data_types": data_types,
            "status": "processing"
        }
        
        # In production:
        # 1. Verify requester's rights
        # 2. Collect requested data
        # 3. Log access request
        # 4. Format data for delivery
        # 5. Update audit log
        
        logger.info(f"Data access request: {request_record}")
        return request_record

    async def handle_data_deletion_request(
        self,
        student_id: int,
        requested_by: str,
        data_types: List[str],
        reason: Optional[str] = None
    ) -> Dict:
        """Handle POPIA data deletion request"""
        deletion_record = {
            "student_id": student_id,
            "requested_by": requested_by,
            "requested_at": datetime.utcnow().isoformat(),
            "data_types": data_types,
            "reason": reason,
            "status": "processing"
        }
        
        # In production:
        # 1. Verify deletion rights
        # 2. Implement data deletion
        # 3. Log deletion request
        # 4. Send confirmation
        # 5. Update audit log
        
        logger.info(f"Data deletion request: {deletion_record}")
        return deletion_record

    async def get_consent_history(
        self,
        student_id: int,
        consent_type: Optional[ConsentType] = None
    ) -> List[Dict]:
        """Get consent history for a student"""
        # In production: Retrieve from database
        return []

    async def schedule_consent_renewal(
        self,
        student_id: int,
        consent_type: ConsentType,
        renewal_date: datetime
    ):
        """Schedule consent renewal notification"""
        renewal_record = {
            "student_id": student_id,
            "consent_type": consent_type.value,
            "renewal_date": renewal_date.isoformat(),
            "status": "scheduled"
        }
        
        # In production:
        # 1. Schedule renewal notification
        # 2. Set up reminders
        # 3. Log scheduling
        
        logger.info(f"Consent renewal scheduled: {renewal_record}")
