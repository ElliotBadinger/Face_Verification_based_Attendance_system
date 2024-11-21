from datetime import datetime
from typing import Optional, Dict, List
import json
import logging
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class AuditEventType(Enum):
    """Types of audit events"""
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    CONSENT_CHANGE = "consent_change"
    AUTHENTICATION = "authentication"
    FACE_RECOGNITION = "face_recognition"
    SYSTEM_CONFIG = "system_config"
    SECURITY_EVENT = "security_event"

class AuditSeverity(Enum):
    """Severity levels for audit events"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AuditLogger:
    """Handles comprehensive audit logging for POPIA compliance"""
    
    def __init__(self, db_session):
        self.db_session = db_session

    async def log_event(
        self,
        event_type: AuditEventType,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        details: Dict,
        severity: AuditSeverity = AuditSeverity.INFO,
        ip_address: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict:
        """Log an audit event"""
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        audit_entry = {
            "event_id": event_id,
            "timestamp": timestamp.isoformat(),
            "event_type": event_type.value,
            "severity": severity.value,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "details": details,
            "ip_address": ip_address,
            "location": location,
            "metadata": {
                "system_version": "1.0.0",
                "correlation_id": self._get_correlation_id()
            }
        }
        
        # In production: Save to secure audit log storage
        logger.info(f"Audit event logged: {audit_entry}")
        return audit_entry

    async def log_data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        purpose: str,
        accessed_fields: List[str],
        ip_address: Optional[str] = None
    ):
        """Log data access event"""
        return await self.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action="access",
            details={
                "purpose": purpose,
                "accessed_fields": accessed_fields,
                "access_type": "read"
            },
            ip_address=ip_address
        )

    async def log_data_modification(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        old_value: Dict,
        new_value: Dict,
        ip_address: Optional[str] = None
    ):
        """Log data modification event"""
        return await self.log_event(
            event_type=AuditEventType.DATA_MODIFICATION,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            details={
                "old_value": old_value,
                "new_value": new_value,
                "modified_fields": self._get_modified_fields(old_value, new_value)
            },
            ip_address=ip_address
        )

    async def log_security_event(
        self,
        user_id: str,
        event_type: str,
        details: Dict,
        severity: AuditSeverity,
        ip_address: Optional[str] = None
    ):
        """Log security-related event"""
        return await self.log_event(
            event_type=AuditEventType.SECURITY_EVENT,
            user_id=user_id,
            resource_type="security",
            resource_id="system",
            action=event_type,
            details=details,
            severity=severity,
            ip_address=ip_address
        )

    async def get_audit_trail(
        self,
        resource_id: Optional[str] = None,
        user_id: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Dict:
        """Retrieve audit trail with filtering and pagination"""
        # In production: Implement database query with filters
        return {
            "total": 0,
            "page": page,
            "page_size": page_size,
            "events": []
        }

    async def export_audit_logs(
        self,
        start_date: datetime,
        end_date: datetime,
        format: str = "json"
    ) -> bytes:
        """Export audit logs for compliance reporting"""
        # In production: Implement secure log export
        return b""

    def _get_correlation_id(self) -> str:
        """Get current correlation ID for request tracing"""
        # In production: Implement request tracing
        return str(uuid.uuid4())

    def _get_modified_fields(self, old_value: Dict, new_value: Dict) -> List[str]:
        """Compare old and new values to determine modified fields"""
        modified_fields = []
        all_keys = set(old_value.keys()) | set(new_value.keys())
        
        for key in all_keys:
            old_val = old_value.get(key)
            new_val = new_value.get(key)
            if old_val != new_val:
                modified_fields.append(key)
                
        return modified_fields

    async def cleanup_old_logs(self, retention_days: int):
        """Clean up old audit logs based on retention policy"""
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        # In production: Implement secure log cleanup
        logger.info(f"Cleaning up audit logs older than {cutoff_date}")
